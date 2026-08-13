from app.plugin.base import BasePlugin, PluginContext, PluginResult
from app.agent.llm import LLMClient
import json
import matplotlib.pyplot as plt
from io import BytesIO


class ChartPlugin(BasePlugin):

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    @property
    def name(self) -> str:
        return "chart"

    @property
    def description(self) -> str:
        return ("Creates a chart specification from query results. "
        "Use this when the user requests a chart, graph, "
        "visualization, or visual representation of data. "
        "This tool should be used after the query tool.")

    @property
    def accepts_upstream(self) -> tuple[str, ...]:
        return ("query",)

    async def execute(
        self,
        context: PluginContext,
        question: str,
    ) -> PluginResult:

        query_data = context.memory.get("query")

        if not query_data:
            raise ValueError(
                "ChartPlugin requires query results."
            )

        prompt = f"""
You are a data visualization assistant.

User question:
{question}

Query result:
{json.dumps(query_data, default=str)}

Create an appropriate chart specification.

Return ONLY valid JSON.

The JSON must have exactly these fields:

{{
    "chart_type": "bar",
    "title": "Chart title",
    "x_field": "field from the data",
    "y_field": "field from the data"
}}

Choose the most appropriate chart_type based on the data.
Allowed chart types:
- bar
- line
- pie

Do not include markdown or ```json.
"""

        response = await self.llm_client.generate(prompt)

        try:
            chart_spec = json.loads(response)
        except json.JSONDecodeError as exc:
            raise ValueError(
                "LLM returned invalid chart JSON."
            ) from exc

        required_fields = {
            "chart_type",
            "title",
            "x_field",
            "y_field",
        }

        if not required_fields.issubset(chart_spec):
            raise ValueError(
                "Chart specification is missing required fields."
            )

        return PluginResult(
            plugin=self.name,
            success=True,
            data=chart_spec,
            metadata={
                "source": "query",
            },
        )
    def render_png(
        self,
        chart_spec: dict,
        query_data: list[dict],
    ) -> bytes:

        chart_type = chart_spec.get("chart_type")
        title = chart_spec.get("title", "Chart")
        x_field = chart_spec.get("x_field")
        y_field = chart_spec.get("y_field")

        print("\nRendering chart:")
        print("Chart type:", chart_type)
        print("X field:", x_field)
        print("Y field:", y_field)

        if not x_field or not y_field:
            raise ValueError(
                "x_field or y_field missing from chart specification"
            )

        if not query_data:
            raise ValueError("No query data available")

        x_values = [
            row[x_field]
            for row in query_data
        ]

        y_values = [
            row[y_field]
            for row in query_data
        ]

        plt.figure(figsize=(10, 6))

        if chart_type == "bar":

            plt.bar(
                x_values,
                y_values,
            )

        else:
            raise ValueError(
                f"Unsupported chart type: {chart_type}"
            )

        plt.title(title)
        plt.xlabel(x_field)
        plt.ylabel(y_field)

        plt.xticks(
            rotation=45,
            ha="right",
        )

        plt.tight_layout()

        buffer = BytesIO()

        plt.savefig(
            buffer,
            format="png",
            dpi=150,
        )

        plt.close()

        buffer.seek(0)

        return buffer.getvalue()
            

    def tool_spec(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "Natural language chart request",
                    }
                },
                "required": ["question"],
            },
        }
