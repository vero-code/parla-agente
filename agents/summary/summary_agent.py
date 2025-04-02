# agents/summary_agent.py
import os
from uagents import Agent, Context, Model
from uagents.protocol import Protocol
from dotenv import load_dotenv

load_dotenv()

class SummaryRequest(Model):
    text: str

class SummaryResponse(Model):
    summary: str

SUMMARY_AGENT_SEED = os.getenv("SUMMARY_AGENT_SEED", "summary-agent-secret-phrase")

summary_agent = Agent(
    name="summary_agent",
    seed=SUMMARY_AGENT_SEED,
    port=8002,
    mailbox=True
)

summary_protocol = Protocol(name="summary-protocol")

@summary_protocol.on_message(model=SummaryRequest)
async def handle_summary(ctx: Context, sender: str, msg: SummaryRequest):
    ctx.logger.info(f"📥 Received text to summarize:\n{msg.text}")

    sentences = msg.text.split(". ")
    summary = ". ".join(sentences[:2]).strip() + "."

    ctx.logger.info(f"📝 Summary: {summary}")
    await ctx.send(sender, SummaryResponse(summary=summary))

summary_agent.include(summary_protocol)

if __name__ == "__main__":
    try:
        summary_agent.run()
    except KeyboardInterrupt:
        print("🛑 Agent stopped by user.")