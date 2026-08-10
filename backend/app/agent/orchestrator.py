from sqlalchemy.ext.asyncio import AsyncSession

from app.agent.llm import LLMClient
from app.plugin.base import PluginContext
from app.plugin.registry import PluginRegistry


class AgentOrchestrator:

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
        session: AsyncSession,
    ):

        context = PluginContext()

        tools = self.registry.tool_specs()

        response = await self.llm_client.generate_with_tools(
            prompt=question,
            tools=tools,
        )

        function_calls = response.function_calls

        if not function_calls:
            return response.text

        function_call = function_calls[0]

        plugin = self.registry.get(function_call.name)

        if plugin is None:
            raise ValueError(
                f"Unknown plugin: {function_call.name}"
            )

        result = await plugin.execute(
            context=context,
            session=session,
            **function_call.args,
        )

        context.memory[plugin.name] = result.data

        return result