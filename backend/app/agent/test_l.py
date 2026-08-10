import asyncio

from app.agent.llm import LLMClient
from app.agent.orchestrator import AgentOrchestrator
from app.plugin.query_plugin import QueryPlugin
from app.plugin.registry import PluginRegistry
from app.db.database import session_local


async def main():

    llm = LLMClient()

    query_plugin = QueryPlugin(llm)

    registry = PluginRegistry()
    registry.register(query_plugin)

    orchestrator = AgentOrchestrator(
        llm_client=llm,
        registry=registry,
    )

    async with session_local() as session:

        result = await orchestrator.run(
            question="What are the top 5 servers by message count?",
            session=session,
        )

        print("\nResult:")
        print(result)


if __name__ == "__main__":
    asyncio.run(main())