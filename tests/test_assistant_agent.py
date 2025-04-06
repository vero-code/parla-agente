# tests/test_assistant_agent.py
import os
import asyncio
from uagents import Agent, Context, Model
from uagents.protocol import Protocol
from dotenv import load_dotenv

load_dotenv()

class AssistantInput(Model):
    user_message: str
    reply_to: str

class AssistantOutput(Model):
    agent_reply: str
    summary: str

class SummaryTrigger(Model):
    pass

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

conversation_done = False

ASSISTANT_AGENT_HOSTED_ADDRESS = os.getenv("ASSISTANT_AGENT_HOSTED_ADDRESS")
if ASSISTANT_AGENT_HOSTED_ADDRESS is None:
    raise ValueError("ASSISTANT_AGENT_HOSTED_ADDRESS environment variable is not set.")

@test_protocol.on_message(model=AssistantOutput)
async def handle_output(ctx: Context, sender: str, msg: AssistantOutput):
    global waiting, current, conversation_done

    if conversation_done:
        if msg.summary and msg.summary != "...":
            ctx.logger.info(f"📝 Final summary arrived: {msg.summary}")
        else:
            ctx.logger.info("⚠️ Late message arrived after conversation complete. Ignoring.")
        return

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
        conversation_done = True
        ctx.logger.info("✅ Conversation complete.")

        ctx.logger.info("📝 Requesting final summary from Assistant...")
        await ctx.send(
            ASSISTANT_AGENT_HOSTED_ADDRESS,
            SummaryTrigger()
        )

async def send_next_message(ctx):
    global current, waiting

    if waiting:
        return

    msg = messages[current]
    ctx.logger.info(f"📤 User sends: {msg}")
    await ctx.send(
        ASSISTANT_AGENT_HOSTED_ADDRESS,
        AssistantInput(user_message=msg, reply_to=test_assistant_agent.address)
    )
    waiting = True
    current += 1

test_assistant_agent.include(test_protocol)

@test_assistant_agent.on_event("startup")
async def start_conversation(ctx: Context):
    await send_next_message(ctx)

if __name__ == "__main__":
    test_assistant_agent.run()