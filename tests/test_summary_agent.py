# tests/test_summary_agent.py
from uagents import Agent, Context, Model
from uagents.protocol import Protocol

class SummaryRequest(Model):
    text: str

class SummaryResponse(Model):
    summary: str

test_summary_agent = Agent(
    name="test_summary_agent",
    seed="test-summary-seed",
    port=8003,
    mailbox=True
)

summary_protocol = Protocol(name="summary-protocol")

@summary_protocol.on_message(model=SummaryResponse)
async def handle_summary_response(ctx: Context, sender: str, msg: SummaryResponse):
    ctx.logger.info(f"🧾 Got summary:\n{msg.summary}")
    print(f"\n📨 Summary received:\n{msg.summary}\n")

test_summary_agent.include(summary_protocol)

@test_summary_agent.on_event("startup")
async def send_summary_request(ctx: Context):
    long_text = (
        "Artificial intelligence is transforming the world in remarkable ways. "
        "From automating repetitive tasks to enabling complex problem-solving, AI has many applications. "
        "However, it also raises ethical and social questions. "
        "Organizations are working on building responsible AI systems."
    )

    ctx.logger.info(f"🚀 Sending text to summary_agent...")

    await ctx.send(
        "agent1q26kk54smp8ga73at9nnkpnr2urelpfg9yv4k6373p7fyn42efvj6jahxwr",
        SummaryRequest(text=long_text)
    )

if __name__ == "__main__":
    test_summary_agent.run()