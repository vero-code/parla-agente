
# 🤖 Parla Agente

An AI agent that **chats on your behalf** and then sends you a short summary of the conversation. Created for participation in the [Fetch.ai Hackathon](https://devpost.com/software/parla-agente-speaks-for-you-and-does-it-beautifully).

![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)


## 🧠 What the Agent Does

Parla Agente is now a **multi-agent system** designed to simulate natural conversations and deliver concise summaries — so you don’t have to reply to every message.

### 1. `Chat Agent` (hosted on Agentverse)

- Communicates in friendly style

- Powered by **Gemini 2.0 Flash**

- Generates natural, human-like replies

### 2. `Summary Agent` (hosted on Agentverse)

- Takes full conversation history and returns a **brief, friendly summary**

- Uses **Gemini** to identify the real meaning behind casual chats

### 3. `Assistant Agent` (hosted on Agentverse)

- Coordinates the conversation

- Sends your message to the Chat Agent

- Collects replies and sends full history to Summary Agent when the dialogue ends

- Supports dynamic agent search and discovery feature on Agentverse.ai

### 4. `Test Assistant Agent` (local test user)

- Imitates a real user sending multiple messages

- Simulates a full conversation flow for local testing


## 🔍 Agent Discovery (New Feature!)

Instead of hardcoding agent addresses, **Parla Agente** now uses a custom `find_agent()` function to find agents dynamically.

It queries [Agentverse.ai](https://agentverse.ai/) for agents with specific tags like: `["innovationlab"]`

That means:  
✔️ You don’t need to maintain static addresses
✔️ Parla Agente can connect to other participants' public agents
✔️ It’s easier to scale and add new agents in the future


## 💡Example

User sends:
> "Hey! How’s your work? Did you see the news today? Let's catch up soon."

AI replies (via Chat Agent), maintains friendly tone and keeps conversation going.  
When the chat ends, Summary Agent returns:
> "**Summary:** Talked about work, the news, and planned to catch up soon. 🎯"


## ⚙️ Tech Stack

- Python 3.13.2

- pip 25.0.1

- [Fetch.ai uAgents Framework](https://docs.fetch.ai/)

- Google Gemini (`gemini-2.0-flash`)

-  `.env` for secure API keys

- VS Code


## 🚀 How to Run


### 1. Clone the repo and install dependencies:

```bash
python -m  venv  venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install  -r  requirements.txt
```

### 2. Add your .env file:

```
GEMINI_API_KEY=your_google_api_key_here
ASSISTANT_AGENT_ADDRESS=...
```

### 3. Start the agents:

```
python tests/test_assistant_agent.py
```


## 💬 Use Case

Your friend messages you.
Parla Agente chats with them in your tone.
You get a short summary like:
_"She wants to call you this evening."_
No stress. No overload. You stay connected ✨


## 📈 Project Status

✅ Chat Agent (Gemini)

✅ Summary Agent (Gemini)

✅ Assistant coordination logic

✅ Multi-turn conversation flow

✅ Auto-summary after dialogue

✅ Connect to other agents on Agentverse

🕒 Telegram/UI integration (in progress)


## 📜 License

This project is licensed under the [MIT License](LICENSE).