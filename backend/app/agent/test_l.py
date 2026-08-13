import asyncio

from app.agent.llm import LLMClient
from app.plugin.query_plugin import QueryPlugin
from app.plugin.chart_plugin import ChartPlugin
from app.plugin.base import PluginContext
from app.db.database import session_local


async def main():

    llm = LLMClient()

    query_plugin = QueryPlugin(llm)
    chart_plugin = ChartPlugin(llm)

    context = PluginContext()

    async with session_local() as session:

        # 1. Run QueryPlugin
        query_result = await query_plugin.execute(
            context=context,
            question="What are the top 5 servers by message count?",
            session=session,
        )

        print("\nQuery result:")
        print(query_result.data)

        # Store query result in context
        context.memory["query"] = query_result.data

        # 2. Run ChartPlugin
        chart_result = await chart_plugin.execute(
            context=context,
            question="Create a bar chart for the top 5 servers by message count.",
        )

        print("\nChart specification:")
        print(chart_result.data)

        # 3. Render PNG
        png_bytes = chart_plugin.render_png(
            chart_result.data,
            context.memory["query"],
        )

        # 4. Save PNG
        with open("chart.png", "wb") as f:
            f.write(png_bytes)

        print("\nChart saved successfully: chart.png")


if __name__ == "__main__":
    asyncio.run(main())