import os
import requests
from uagents import Agent, Context, Model
from uagents.protocol import Protocol

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class ChatRequest(Model):
    message: str

class ChatResponse(Model):
    reply: str

chat_agent = Agent(
    name="chat_agent",
    seed=os.getenv("CHAT_AGENT_SEED", "chat-agent-secret-phrase"),
    mailbox=True
)

def query_gemini(prompt: str) -> str:
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    try:
        response = requests.post(url, headers=headers, params=params, json=data)
        response.raise_for_status()
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"⚠️ Gemini error: {str(e)}"

chat_protocol = Protocol(name="chat-protocol")

@chat_protocol.on_message(model=ChatRequest)
async def handle_chat(ctx: Context, sender: str, msg: ChatRequest):
    ctx.logger.info(f"🗣 Message received from {sender}: {msg.message}")
    
    try:
        reply = query_gemini(msg.message)
        ctx.logger.info(f"🤖 Gemini reply: {reply}")
    except Exception as e:
        reply = "⚠️ Sorry, something went wrong while processing your request."
        ctx.logger.error(f"Gemini API error: {e}")

    await ctx.send(sender, ChatResponse(reply=reply))

chat_agent.include(chat_protocol)

if __name__ == "__main__":
    chat_agent.run()