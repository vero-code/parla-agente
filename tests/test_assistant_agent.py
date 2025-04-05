# tests/test_assistant_agent.py
import os
import asyncio
from uagents import Agent, Context, Model
from uagents.protocol import Protocol
from dotenv import load_dotenv

load_dotenv()

class AssistantInput(Model):
    user_message: str

class AssistantOutput(Model):
    agent_reply: str
    summary: str

test_assistant_agent = Agent(
    name="test_assistant_agent",
    seed="test-assistant-seed",
    port=8005,
    mailbox=True
)

test_protocol = Protocol(name="assistant-protocol")

messages = [
    "Hey! How's your work?",
    "Did you see the news today?",
    "I'm thinking of going to the beach this weekend.",
    "Do you still play guitar?",
    "Let's catch up soon!"
]

current = 0
waiting = False

@test_protocol.on_message(model=AssistantOutput)
async def handle_output(ctx: Context, sender: str, msg: AssistantOutput):
    global waiting, current

    ctx.logger.info(f"📨 From Chat Agent: {msg.agent_reply}")

    if "⚠️ Sorry, no available chat agent found" in msg.agent_reply:
        ctx.logger.warning("❌ Stopping further messages: Chat agent not available.")
        return

    if msg.summary and msg.summary != "...":
        ctx.logger.info(f"📝 From Summary Agent: {msg.summary}")

    waiting = False

    if current < len(messages):
        await asyncio.sleep(2.5)
        await send_next_message(ctx)
    else:
        ctx.logger.info("✅ Conversation complete.")

ASSISTANT_AGENT_HOSTED_ADDRESS = os.getenv("ASSISTANT_AGENT_HOSTED_ADDRESS")
if ASSISTANT_AGENT_HOSTED_ADDRESS is None:
    raise ValueError("ASSISTANT_AGENT_HOSTED_ADDRESS environment variable is not set.")

async def send_next_message(ctx):
    global current, waiting

    if waiting:
        return

    msg = messages[current]
    ctx.logger.info(f"📤 User sends: {msg}")
    await ctx.send(
        os.getenv("ASSISTANT_AGENT_HOSTED_ADDRESS"),
        AssistantInput(user_message=msg)
    )
    waiting = True
    current += 1

test_assistant_agent.include(test_protocol)

@test_assistant_agent.on_event("startup")
async def start_conversation(ctx: Context):
    await send_next_message(ctx)

if __name__ == "__main__":
    test_assistant_agent.run()