# 🤖 Parla Agente

An AI agent that **chats on your behalf** and then sends you a short summary of the conversation. Created for participation in the [Fetch.ai Hackathon](https://fetch-ai-hackathon.devpost.com/).

![domain:innovation-lab](https://img.shields.io/badge/innovation--lab-3D8BD3)


## 🧠 What the Agent Does

### 1. `Chat Agent`
- Communicates in your style (friendly, casual, or professional)
- Powered by **Gemini** by Google
- Generates natural, conversational replies


## ⚙️ Tech Stack

- Python 3.13.2
- pip 25.0.1
- Google Gemini (`gemini-2.0-flash`)
- `.env` for secure API key handling
- VS Code


## 🚀 How to Run

### 1. Clone the repo and install dependencies:

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Add your .env file:
```
GEMINI_API_KEY=your_google_api_key_here
```

### 3. Test the setup:
```
python agents/chat_agent.py
```


## 💬 Use Case

"Your friend texts you — the AI chats with them in your style,  
then sends you a summary: 'He want to call you.'"


## 🏁 Progress

-   Gemini integration
    
-   First working Chat Agent


## 📜 License

This project is licensed under the [MIT License](LICENSE).