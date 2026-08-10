from app.plugin.base import BasePlugin, PluginContext, PluginResult
from sqlalchemy.ext.asyncio import AsyncSession
from app.agent.prompt import SQL_SYSTEM_PROMPT
from app.core.sql_quard import SQLGuard
from sqlalchemy import text
from app.agent.llm import LLMClient

class QueryPlugin(BasePlugin):
    def __init__(self,llm_client: LLMClient):
        self.llm_client = llm_client

    @property
    def name(self) -> str:
        return "query"

    @property
    def description(self) -> str:
        return "Converts natural language into SQL and returns structured data."

    async def execute(
        self,
        context: PluginContext,
        question: str,
        session: AsyncSession,
    ) -> PluginResult:
        prompt = SQL_SYSTEM_PROMPT.format(question=question)
        sql = await self.llm_client.generate(prompt)

        safe_sql = SQLGuard.validate(sql)

        result = await session.execute(text(safe_sql))
        rows = result.mappings().all()

        return PluginResult(
            plugin=self.name,
            success=True,
            data=[dict(row) for row in rows],
            metadata={"sql": safe_sql,"row_count": len(rows)},
        )

    def tool_spec(self) -> dict:
        return {
        "name": self.name,
        "description": self.description,
        "parameters": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "Natural language analytics question",
                }
            },
            "required": ["question"],
        },
    }
