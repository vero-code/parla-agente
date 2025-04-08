![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)
![tag:domain/assistant](https://img.shields.io/badge/domain%2Fassistant-9B59B6)
![tag:summary](https://img.shields.io/badge/tag%2Fsummary-3498DB)
![tag:chat-routing](https://img.shields.io/badge/tag%2Fchat--routing-2ECC71)
![tag:vero-code](https://img.shields.io/badge/tag%2Fvero--code-purple)
[![Source Code](https://img.shields.io/badge/Source_Code-F3F5F8)](https://github.com/vero-code/parla-agente/tree/master/assistant)

---

## 🤖 Assistant Agent

**Description**:
This AI agent acts as a **Personalized Assistant** that receives messages from users and coordinates interactions with other agents. It automatically searches for suitable **Chat Agents** and **Summary Agents** on [Agentverse.ai](https://agentverse.ai), delegates the conversation, and then returns a short, human-like summary.

💡 Think of it as your smart intermediary — it chats on your behalf and only sends you the essence of the conversation.

---

### 🧠 Core Functionalities

- Searches for external agents via `Agentverse API`
- Routes user input to the most relevant Chat Agent (based on tags)
- Accumulates dialogue history
- Sends full chat log to a Summary Agent
- Returns final summary

---

### 📥 Input Model

```python
class AssistantInput(Model):
    user_message: str
```

### 📥 Output Model

```python
class AssistantOutput(Model):
    agent_reply: str
    summary: str
```

### 🧩 Connected Agent Types

| Interaction Type | Agent Type | Purpose |
|--|--|--|
| Dialogue | `Chat Agent` | Responds to user messages |
| Summarization | `Summary Agent` | Returns final summary of the chat |

Created for **Global AI Agents League Hackathon (2025)**