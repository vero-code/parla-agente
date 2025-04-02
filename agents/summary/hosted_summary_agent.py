# agents/hosted_summary_agent. The agent is hosted at agentverse.ai as Summary Agent
import os
import requests
from uagents import Agent, Context, Model
from uagents.protocol import Protocol

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class SummaryRequest(Model):
    text: str

class SummaryResponse(Model):
    summary: str

SUMMARY_AGENT_SEED = os.getenv("SUMMARY_AGENT_SEED", "summary-agent-secret-phrase")

summary_agent = Agent(
    name="summary_agent",
    seed=SUMMARY_AGENT_SEED,
    mailbox=True
)

def query_gemini(prompt: str) -> str:
    prompt = f"Summarize the gist of the conversation in a very brief and concise manner, like 'Talked about the weather, decided to meet on Friday': '{prompt}'"

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    try:
        response = requests.post(url, headers=headers, params=params, json=data)
        response.raise_for_status()
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"⚠️ Gemini error: {str(e)}"

summary_protocol = Protocol(name="summary-protocol")

@summary_protocol.on_message(model=SummaryRequest)
async def handle_summary(ctx: Context, sender: str, msg: SummaryRequest):
    ctx.logger.info(f"📥 Received text to summarize:\n{msg.text}")

    summary = query_gemini(msg.text)

    ctx.logger.info(f"📝 Summary: {summary}")
    await ctx.send(sender, SummaryResponse(summary=summary))

summary_agent.include(summary_protocol)

if __name__ == "__main__":
    summary_agent.run()