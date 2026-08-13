import json

from app.agent.llm import LLMClient
from app.plugin.base import PluginContext
from app.plugin.registry import PluginRegistry


class AgentOrchestrator:

    MAX_TOOL_CALLS = 5

    def __init__(
        self,
        llm_client: LLMClient,
        registry: PluginRegistry,
    ):
        self.llm_client = llm_client
        self.registry = registry

    async def run(
        self,
        question: str,
        session=None,
    ):

        context = PluginContext(session=session)

        tools = self.registry.tool_specs()

        prompt = question

        for _ in range(self.MAX_TOOL_CALLS):

            response = await self.llm_client.generate_with_tools(
                prompt=prompt,
                tools=tools,
            )

            # LLM decided no more tools are required
            if not response.function_calls:
                return response.text

            for call in response.function_calls:

                plugin = self.registry.get(call.name)

                if plugin is None:
                    raise ValueError(
                        f"Unknown plugin: {call.name}"
                    )

                result = await plugin.execute(
                    context=context,
                    **call.args,
                )

                if not result.success:
                    raise RuntimeError(
                        f"Plugin '{plugin.name}' failed"
                    )

                # Store plugin output
                context.memory[plugin.name] = result.data

                prompt = self._build_next_prompt(
                    question=question,
                    context=context,
                )

        return "I couldn't complete the requested operation."

    def _build_next_prompt(
        self,
        question: str,
        context: PluginContext,
    ) -> str:

        return f"""
You are an intelligent analytics assistant.

Original user question:
{question}

Plugin outputs:
{json.dumps(context.memory, default=str)}

Decide what to do next.

If another available plugin is required,
call the appropriate plugin.

If the request has already been satisfied,
answer the user directly.

Do not generate SQL yourself.
"""