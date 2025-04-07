from uagents import Model

class UserbotInput(Model):
    text: str

class AssistantInput(Model):
    user_message: str
    reply_to: str

class AssistantOutput(Model):
    agent_reply: str
    summary: str