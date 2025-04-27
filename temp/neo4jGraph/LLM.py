import random
import string
from typing import Any, List, Optional, Union
import asyncio

from openai import OpenAI
from neo4j_graphrag.llm import LLMInterface, LLMResponse
from neo4j_graphrag.message_history import MessageHistory
from neo4j_graphrag.types import LLMMessage

class CustomLLM(LLMInterface):
    def __init__(self, model_name: str = None, system_instruction: Optional[str] = None, **kwargs: Any):
        # 请替换 "<DeepSeek API Key>" 为你的实际 DeepSeek API key
        self.client = OpenAI(api_key="sk-000c2ac6c4164fb882a676b467323439", base_url="https://api.deepseek.com")
        self.model = "deepseek-chat"
        self.max_tokens = 1024

    def invoke(
        self,
        input: str,
        message_history: Optional[Union[List[LLMMessage], MessageHistory]] = None,
        system_instruction: Optional[str] = None,
    ) -> LLMResponse:
        messages = [{"role": "user", "content": input}]
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=self.max_tokens,
        )
        # 假设响应类似于 OpenAI 的 ChatCompletion
        response_text = response.choices[0].message.content
        return LLMResponse(content=response_text)

    async def ainvoke(
        self,
        input: str,
        message_history: Optional[Union[List[LLMMessage], MessageHistory]] = None,
        system_instruction: Optional[str] = None,
    ) -> LLMResponse:
        # 模拟异步调用
        await asyncio.sleep(1)  # 模拟异步操作
        messages = [{"role": "user", "content": input}]
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=self.max_tokens,
        )
        response_text = response.choices[0].message.content
        return LLMResponse(content=response_text)

# 示例调用
if __name__ == "__main__":
    llm = CustomLLM()
    res: LLMResponse = llm.invoke("text")
    print(res.content)

    # 异步调用示例
    async def main():
        llm = CustomLLM()
        res: LLMResponse = await llm.ainvoke