# 🤖 Chat Agent

![tag:innovation-lab](https://img.shields.io/badge/innovation--lab-3D8BD3)
![tag:domain/chat](https://img.shields.io/badge/domain%2Fchat-blue)
![tag:vero-git-hub](https://img.shields.io/badge/tag%2Fvero--git--hub-purple)
![tag:gemini-ai](https://img.shields.io/badge/tag%2Fgemini--ai-green)
![domain:chat](https://img.shields.io/badge/chat-3D8BD3)


## 🎯 **Purpose**
The **Chat Agent** is an intelligent microservice that handles incoming natural language queries and generates responses using **Google Gemini AI**.


### 🧠 **Functionalities**

-   Accepts user messages via the `ChatRequest` model
    
-   Generates smart responses using **Gemini 2.0 Flash** (`ChatResponse`)
    
-   Acts as a conversational core inside multi-agent systems (e.g., **Assistant Agent**)
    
-   Can be queried independently by other microservices
    

### 💼 **Use Cases**

-   **Conversational AI** – Answering user queries in natural language
    
-   **Multilingual Q&A** – Understanding multiple languages via Gemini
    
-   **Integrated Chat Systems** – Used as a module in larger agent pipelines
    
-   **Hackathon-ready AI Microservice** – Lightweight, hosted, and ready to scale
    

### 🤝 **Interactions**

| Interaction Type |  Agent | Purpose |
|------------------|--------|---------|
| 🧠 Dialogue | `Assistant Agent` | Sends messages for natural language replies |
| ✂️ Summarization | `Summary Agent` | Processes full conversation history |


### ****Input / Output Models****

```python
class ChatRequest(Model):
    message: str

class ChatResponse(Model):
    reply: str

```

### 👤 **Agent on Agentverse**

You can view more details about this agent on [Agentverse](https://agentverse.ai/agents/details/agent1qttk8danzs0tuyj6drs332fxsk05z9acycakhrgyqxyxn0ky50yugvwcn6u).

_Hackathon Participant – Global AI Agents League (Fetch.ai, 2025)_

This agent supports `chat`, is powered by `Gemini AI`, and can be found under the name `chat_agent`. It's part of the `domain:chat` group and acts as an intelligent `agent` for natural language processing.