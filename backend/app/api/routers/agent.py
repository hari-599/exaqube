from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.agent.orchestrator import AgentOrchestrator
from app.agent.llm import LLMClient
from app.plugin.registry import PluginRegistry
from app.plugin.query_plugin import QueryPlugin
from app.plugin.chart_plugin import ChartPlugin
from app.db.database import session_local


router = APIRouter(prefix="/agent", tags=["Agent"])


class AgentRequest(BaseModel):
    question: str


class AgentResponse(BaseModel):
    answer: str


def get_orchestrator() -> AgentOrchestrator:
    llm = LLMClient()

    registry = PluginRegistry()
    registry.register(QueryPlugin(llm))
    registry.register(ChartPlugin(llm))

    return AgentOrchestrator(
        llm_client=llm,
        registry=registry,
    )


async def get_db():
    async with session_local() as session:
        yield session


@router.post("/ask", response_model=AgentResponse)
async def ask_agent(
    request: AgentRequest,
    session: AsyncSession = Depends(get_db),
):
    orchestrator = get_orchestrator()

    result = await orchestrator.run(
        question=request.question,
        session=session,
    )

    return AgentResponse(answer=result)