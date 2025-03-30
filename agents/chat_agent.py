# agents/chat_agent
import os
from uagents import Agent, Context, Model
from uagents.protocol import Protocol
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class ChatRequest(Model):
    message: str

class ChatResponse(Model):
    reply: str

CHAT_AGENT_SEED = os.getenv("CHAT_AGENT_SEED", "chat-agent-secret-phrase")

chat_agent = Agent(
    name="chat_agent",
    seed=CHAT_AGENT_SEED,
    port=8001,
    mailbox=True
)

model = genai.GenerativeModel(model_name="models/gemini-2.0-flash")

chat_protocol = Protocol(name="chat-protocol")

@chat_protocol.on_message(model=ChatRequest)
async def handle_chat(ctx: Context, sender: str, msg: ChatRequest):
    ctx.logger.info(f"🗣 Received: {msg.message}")
    # response = model.generate_content(msg.message)
    # reply = response.text
    reply = "I'm doing well, thank you for asking! As a large language model, I don't experience emotions or feelings in the same way humans do, but I'm functioning optimally and ready to assist you with your requests. How are you doing today?"
    ctx.logger.info(f"🤖 Responding: {reply}")

    await ctx.send(sender, ChatResponse(reply=reply))

chat_agent.include(chat_protocol)

if __name__ == "__main__":
    try:
        chat_agent.run()
    except KeyboardInterrupt:
        print("🛑 Agent stopped by user.")