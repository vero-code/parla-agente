# agents/hosted_chat_agent. The agent is hosted at agentverse.ai as Chat Agent
import os
import requests
from uagents import Agent, Context, Model
from uagents.protocol import Protocol

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class ChatRequest(Model):
    message: str
    reply_to: str

class ChatResponse(Model):
    reply: str
    reply_to: str

chat_agent = Agent(
    name="chat_agent",
    seed=os.getenv("CHAT_AGENT_SEED", "chat-agent-secret-phrase"),
    mailbox=True
)

def query_gemini(prompt: str) -> str:
    prompt = f"Reply as a friendly conversationalist, keeping it brief and positive. The message is: '{prompt}'. Avoid gendered pronouns and verb forms. Keep it short and lighthearted, and respond only in the language of the original message."

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    response = requests.post(url, headers=headers, params=params, json=data)
    response.raise_for_status()

    return response.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")

chat_protocol = Protocol(name="chat-protocol")

@chat_protocol.on_message(model=ChatRequest)
async def handle_chat(ctx: Context, sender: str, msg: ChatRequest):
    ctx.logger.info(f"🗣 Message received from {sender}: {msg.message}")
    
    try:
        reply = query_gemini(msg.message)
        ctx.logger.info(f"🤖 Gemini reply: {reply}")
    except Exception as e:
        reply = "😅 Oops, I had a moment... Could you say that again?"
        ctx.logger.error(f"Gemini API error: {e}")

    await ctx.send(sender, ChatResponse(reply=reply, reply_to=msg.reply_to))

chat_agent.include(chat_protocol)

if __name__ == "__main__":
    chat_agent.run()