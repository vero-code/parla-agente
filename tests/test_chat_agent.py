# tests/test_chat_agent
from uagents import Agent, Context, Model
from uagents.protocol import Protocol

class ChatRequest(Model):
    message: str

class ChatResponse(Model):
    reply: str

test_agent = Agent(
    name="test_agent",
    seed="test-seed-phrase",
    port=8000,
    mailbox=True
)

test_protocol = Protocol(name="chat-protocol")

@test_protocol.on_message(model=ChatResponse)
async def handle_response(ctx: Context, sender: str, msg: ChatResponse):
    ctx.logger.info(f"📨 Got reponse from chat_agent:\n{msg.reply}")

test_agent.include(test_protocol)

@test_agent.on_event("startup")
async def test_send(ctx: Context):
    message = "Hi! How are you doing?"
    ctx.logger.info(f"🔗 Sending to chat_agent: {message}")

    await ctx.send(
        "agent1qfsxzdvy4vxtxrtllsfp8gxq4ssgkl50elsklrhf0fhjkynsfmcmg3dl3w0",
        ChatRequest(message=message)
    )

if __name__ == "__main__":
    test_agent.run()