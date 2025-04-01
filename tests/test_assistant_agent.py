# tests/test_assistant_agent.py
import os
from uagents import Agent, Context, Model
from uagents.protocol import Protocol

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

@test_protocol.on_message(model=AssistantOutput)
async def handle_output(ctx: Context, sender: str, msg: AssistantOutput):
    ctx.logger.info(f"📨 From Chat Agent: {msg.agent_reply}")
    ctx.logger.info(f"📝 From Summary Agent: {msg.summary}")

test_assistant_agent.include(test_protocol)

@test_assistant_agent.on_event("startup")
async def send_message(ctx: Context):
    user_msg = "Hey! How is your work? Why haven't you called for a long time?"
    ctx.logger.info(f"📤 User sends message to assistant: {user_msg}")
    await ctx.send(
        os.getenv("ASSISTANT_AGENT_ADDRESS"),
        AssistantInput(user_message=user_msg)
    )

if __name__ == "__main__":
    test_assistant_agent.run()