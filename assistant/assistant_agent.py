# assistant/assistant_agent.py
import os
from uagents import Agent, Context, Model
from uagents.protocol import Protocol
from dotenv import load_dotenv

load_dotenv()

class AssistantInput(Model):
    user_message: str

class AssistantOutput(Model):
    agent_reply: str
    summary: str

class ChatRequest(Model):
    message: str

class ChatResponse(Model):
    reply: str

class SummaryRequest(Model):
    text: str

class SummaryResponse(Model):
    summary: str

ASSISTANT_AGENT_SEED = os.getenv("ASSISTANT_AGENT_SEED", "assistant-agent-secret-phrase")

assistant_agent = Agent(
    name="assistant_agent",
    seed=ASSISTANT_AGENT_SEED,
    port=8004,
    mailbox=True
)

conversation_history = []
last_sender = None

assistant_protocol = Protocol(name="assistant-protocol")

@assistant_protocol.on_message(model=AssistantInput)
async def handle_assistant(ctx: Context, sender: str, msg: AssistantInput):
    global last_sender
    ctx.logger.info(f"🧾 Assistant received message: {msg.user_message}")
    conversation_history.append(f"User: {msg.user_message}")
    last_sender = sender

    await ctx.send(
        os.getenv("CHAT_AGENT_ADDRESS"),
        ChatRequest(message=msg.user_message)
    )

@assistant_agent.on_message(model=ChatResponse)
async def handle_chat_reply(ctx: Context, sender: str, msg: ChatResponse):
    ctx.logger.info(f"💬 Chat reply: {msg.reply}")
    conversation_history.append(f"Agent: {msg.reply}")

    full_text = " ".join(conversation_history)
    await ctx.send(
        os.getenv("SUMMARY_AGENT_ADDRESS"),
        SummaryRequest(text=full_text)
    )

@assistant_agent.on_message(model=SummaryResponse)
async def handle_summary(ctx: Context, sender: str, msg: SummaryResponse):
    global last_sender
    ctx.logger.info(f"📝 Summary received: {msg.summary}")
    response = AssistantOutput(
        agent_reply=conversation_history[-1].replace("Agent: ", ""),
        summary=msg.summary
    )
    await ctx.send(last_sender, response)

assistant_agent.include(assistant_protocol)

if __name__ == "__main__":
    assistant_agent.run()