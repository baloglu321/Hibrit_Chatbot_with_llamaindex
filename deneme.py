import os
import gradio as gr
import requests
from agent import *
import random
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core.workflow import Context
import asyncio
import nest_asyncio

nest_asyncio.apply()


class BasicAgent:

    def __init__(self):
        print("BasicAgent initialized.")
        self.agent = build_agent()
        self.memory = ChatMemoryBuffer.from_defaults(token_limit=40000)

    async def __call__(self, question: str) -> str:
        print(f"Agent received question (first 50 chars): {question[:50]}...")
        ctx = Context(self.agent)
        fixed_answer = await self.agent.run(question, ctx=ctx, memory=self.memory)
        if not isinstance(fixed_answer, (str, int, float)):
            fixed_answer = str(fixed_answer)
        # print(f"Agent returning fixed answer: {fixed_answer}")
        print(self.memory.get_all())
        return fixed_answer


try:
    agent = BasicAgent()
except Exception as e:
    print(f"Error instantiating agent: {e}")

soru = "Türkiye'nin başkenti neresidir?"

# Konuşma geçmişi (Gradio'dan gelen liste formatında olmalı)

try:
    # Agent'ı asenkron olarak çalıştır
    cevap = asyncio.run(agent(question=soru))

    print(f"Agent'tan Gelen Cevap: {cevap}")

except Exception as e:
    print(f"Agent çalıştırılırken hata oluştu: {e}")
