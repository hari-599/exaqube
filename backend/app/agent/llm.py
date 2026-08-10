from google import genai
from dotenv import load_dotenv
import os
from google.genai import types

load_dotenv()


class LLMClient:

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = os.getenv("GEMINI_MODEL")

        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not set")

        if not self.model:
            raise ValueError("GEMINI_MODEL is not set")

        self.client = genai.Client(api_key=self.api_key)

    async def generate(self, prompt: str) -> str:
        response = await self.client.aio.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        return response.text

    async def generate_with_tools(
        self,
        prompt: str,
        tools: list[dict],
    ):
        declarations = [
            types.FunctionDeclaration(
                name=tool["name"],
                description=tool["description"],
                parameters_json_schema=tool.get("parameters", {}),
            )
            for tool in tools
        ]

        gemini_tools = [
            types.Tool(
                function_declarations=declarations
            )
        ]

        response = await self.client.aio.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=gemini_tools,
                automatic_function_calling=types.AutomaticFunctionCallingConfig(
                    disable=True
                ),
            ),
        )

        return response