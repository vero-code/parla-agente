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
    ctx.logger.info("📨 Answer received from assistant:")
    ctx.logger.info(f"💬 Agent's response: {msg.agent_reply}")
    ctx.logger.info(f"📝 Summary: {msg.summary}")
    print("\n📥 Assistant Reply:", msg.agent_reply)
    print("📄 Summary:", msg.summary)

test_assistant_agent.include(test_protocol)

@test_assistant_agent.on_event("startup")
async def send_message(ctx: Context):
    user_msg = "Hello! I'm planning a trip to Paris and want to know the best time to go."
    ctx.logger.info(f"📤 Sending a message to your assistant: {user_msg}")
    await ctx.send(
        os.getenv("ASSISTANT_AGENT_ADDRESS"),
        AssistantInput(user_message=user_msg)
    )

if __name__ == "__main__":
    test_assistant_agent.run()