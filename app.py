import os
import gradio as gr
import requests
from agent import *
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.workflow import Context
import asyncio
import nest_asyncio

nest_asyncio.apply()

CLOUDFLARE_TUNNEL_URL = "..."
OLLAMA_MODEL_ID = "gemma3:27b"


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

        return fixed_answer


try:
    agent = BasicAgent()
except Exception as e:
    print(f"Error instantiating agent: {e}")


def basic_response(message: str, history: list) -> str:
    """Basit, genel sohbet sorularını cevaplar."""
    print("-> Basic Response modülü çalışıyor.")
    system_prompt = "You are a helpful and friendly assistant. Keep your answers concise and conversational. Do not respond in any other language. Even if your internal reasoning is in English, translate the final answer back to the user's language before returning it."

    messages = [{"role": "system", "content": system_prompt}]

    # History elemanlarını dolaş ve formatı normalize et
    for item in history:
        user_msg = None
        assistant_msg = None

        # 1. Kontrol: Eski/Basit Format (Tuple/Liste)
        if isinstance(item, (list, tuple)) and len(item) == 2:
            user_msg, assistant_msg = item

        # 2. Kontrol: Yeni/Karmaşık Format (Dict/Gradio İç Formatı)
        elif isinstance(item, dict) and "role" in item and "content" in item:
            continue  # Karmaşık formatı atla, sadece basit tuple çiftlerini işle.

        if user_msg and assistant_msg:
            messages.append({"role": "user", "content": user_msg})
            messages.append({"role": "assistant", "content": assistant_msg})

    # Mevcut soruyu en sona ekle
    messages.append({"role": "user", "content": message})

    # print(f"LLM'e gönderilen son mesaj listesi: {messages}") # Debug için açılabilir
    return call_llm(messages)


def call_llm(message: str) -> str:
    url = f"{CLOUDFLARE_TUNNEL_URL}api/chat"
    headers = {"Content-Type": "application/json"}

    data = {"model": "gemma3:27b", "stream": False, "messages": message}
    response = requests.post(url, headers=headers, data=json.dumps(data), stream=True)
    full_response = ""
    for line in response.iter_lines():
        if line:
            json_data = json.loads(line.decode("utf-8"))
            content = json_data.get("message", {}).get("content", "")
            full_response += content
    # print(full_response)
    return full_response


def route_question(message: str) -> str:
    """
    Kullanıcının sorusunu analiz eder ve 'AGENT' veya 'BASIC' olarak sınıflandırır.
    Bu fonksiyon, sistemin beynidir.
    """
    print(f"Yönlendirme için soru analiz ediliyor: '{message[:50]}...'")

    # Router'a özel, çok net bir sistem talimatı veriyoruz.
    system_prompt = (
        "You are an expert routing assistant. Your task is to classify the user's query. "
        "If the query requires real-time information, access to external tools (like web search, calculations, file access), "
        "or is a complex question that a simple chat model cannot answer, respond with only the single word: AGENT. "
        "For all other general conversational queries, greetings, simple questions, or chit-chat, respond with only the single word: BASIC."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": message},
    ]

    # Daha küçük ve hızlı bir model kullanmak burada maliyeti ve hızı artırabilir.
    decision = call_llm(messages)  # Örnek olarak daha küçük bir model

    # Çıktının sadece "AGENT" veya "BASIC" olduğundan emin olalım.
    decision_clean = "AGENT" if "AGENT" in decision.upper() else "BASIC"
    print(f"Yönlendirme Kararı: {decision_clean}")
    return decision_clean


def hybrid_response_with_router(message: str, history: list):
    """
    Gradio arayüzünün ana giriş noktası.
    Önce soruyu yönlendirir, sonra ilgili fonksiyonu çağırır.
    'yield' kullanarak arayüzü aşamalı olarak günceller.
    """
    # 1. Adım: Sorunun nereye gideceğine karar ver.
    decision = route_question(message)

    # 2. Adım: Karara göre ilgili fonksiyonu çalıştır.
    if decision == "AGENT":
        # Kullanıcıya bekleyeceğini bildir.
        yield "Agent'ı devreye alıyorum, bu işlem biraz zaman alabilir... ⏳"
        # Agent'ı çalıştır ve sonucu al.
        response = asyncio.run(agent(message))
        yield response
    else:  # decision == "BASIC"
        response = basic_response(message, history)
        yield response


gr.ChatInterface(
    fn=hybrid_response_with_router,
    title="🤖 Hibrit Chatbot & Agent Sistemi",
    description="Soru sorun. Sistem, sorunun basit mi yoksa karmaşık mı olduğuna karar verip ilgili modülü çalıştıracaktır.",
    examples=[
        ["Selam, naber?"],
        ["Türkiye'nin güncel nüfusu ne kadar?"],
        ["Bugün İstanbul'da hava nasıl?"],
    ],
).launch()
