import asyncio

from app.agent.llm import LLMClient
from app.agent.prompt import SQL_SYSTEM_PROMPT
from app.core.sql_quard import SQLGuard, SQLGuardError

async def main():
    llm = LLMClient()

    question = "Show me the top 5 servers by message count."

    prompt = SQL_SYSTEM_PROMPT.format(question=question)

    sql = await llm.generate(prompt)
    val_sql = SQLGuard.validate(sql)
    print("Validated SQL:")
    print(val_sql)


if __name__ == "__main__":
    asyncio.run(main())