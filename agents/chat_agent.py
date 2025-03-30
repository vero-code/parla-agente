import os
from uagents import Agent, Context, Model
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
    endpoint=["http://localhost:8001/submit"]
)

model = genai.GenerativeModel(model_name="models/gemini-2.0-flash")

@chat_agent.on_message(model=ChatRequest)
async def handle_chat(ctx: Context, sender: str, msg: ChatRequest):
    ctx.logger.info(f"🗣 Received: {msg.message}")
    response = model.generate_content(msg.message)
    reply = response.text
    ctx.logger.info(f"🤖 Responding: {reply}")

    await ctx.send(sender, ChatResponse(reply=reply))

if __name__ == "__main__":
    chat_agent.run()