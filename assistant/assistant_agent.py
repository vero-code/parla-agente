# assistant/assistant_agent.py
import os
import requests
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
AGENTVERSE_API_KEY = os.getenv("AGENTVERSE_API_KEY")

assistant_agent = Agent(
    name="assistant_agent",
    seed=ASSISTANT_AGENT_SEED,
    port=8004,
    mailbox=True
)

conversation_history = []
last_sender = None

def find_agent(search_text="chat", limit=3):
    payload = {
        "filters": {},
        "sort": "relevancy",
        "direction": "asc",
        "search_text": "chat",
        "offset": 0,
        "limit": 5
    }

    headers = {
        "Authorization": f"Bearer {AGENTVERSE_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            "https://agentverse.ai/v1/search/agents",
            headers=headers,
            json=payload
        )

        print("📤 Search Payload:")
        print(payload)

        if response.status_code != 200:
            print(f"❌ Request failed: {response.status_code}")
            print("🔴 Response:", response.text)
            return None

        data = response.json()
        agents = data.get("agents", [])
        if not agents:
            print("⚠️ No agents found.")
            return None
        
        for i, agent in enumerate(agents):
            print(f"\n✅ Agent #{i+1}")
            print(f"Name: {agent.get('name')}")
            print(f"Address: {agent.get('address')}")
            print(f"Status: {agent.get('status')}")
            print(f"README tags: {agent.get('readme', '')[:200]}...")

        return agents[0].get("address")

    except Exception as e:
        print(f"❌ Exception during search: {e}")
        return None

assistant_protocol = Protocol(name="assistant-protocol")

@assistant_protocol.on_message(model=AssistantInput)
async def handle_assistant(ctx: Context, sender: str, msg: AssistantInput):
    global last_sender
    ctx.logger.info(f"🧾 Assistant received message: {msg.user_message}")
    conversation_history.append(f"User: {msg.user_message}")
    last_sender = sender

    chat_address = find_agent()

    if not chat_address:
        ctx.logger.error("❌ Chat agent not found via REST API.")
        await ctx.send(sender, AssistantOutput(
            agent_reply="⚠️ Sorry, no available chat agent found.",
            summary="Chat agent unavailable."
        ))
        return

    ctx.logger.info(f"🔍 Found ChatAgent at: {chat_address}")
    await ctx.send(chat_address, ChatRequest(message=msg.user_message))

@assistant_agent.on_message(model=ChatResponse)
async def handle_chat_reply(ctx: Context, sender: str, msg: ChatResponse):
    ctx.logger.info(f"💬 Chat Agent reply: {msg.reply}")
    conversation_history.append(f"Agent: {msg.reply}")

    await ctx.send(last_sender, AssistantOutput(agent_reply=msg.reply, summary="..."))

    if len(conversation_history) >= 10:
        summary_address = os.getenv("SUMMARY_AGENT_HOSTED_ADDRESS")
        full_text = " ".join(conversation_history)
        await ctx.send(
            summary_address,
            SummaryRequest(text=full_text)
        )

@assistant_agent.on_message(model=SummaryResponse)
async def handle_summary(ctx: Context, sender: str, msg: SummaryResponse):
    global last_sender
    ctx.logger.info(f"📝 Summary Agent: {msg.summary}")
    response = AssistantOutput(
        agent_reply=conversation_history[-1].replace("Agent: ", ""),
        summary=msg.summary
    )
    await ctx.send(last_sender, response)

assistant_agent.include(assistant_protocol)

if __name__ == "__main__":
    assistant_agent.run()