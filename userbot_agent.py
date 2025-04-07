# userbot_agent.py
import os
import asyncio
from telethon import TelegramClient, events
from dotenv import load_dotenv
from uagents import Agent, Context
from models import UserbotInput, AssistantInput, AssistantOutput, SummaryTrigger

load_dotenv()

API_ID = int(os.getenv("TG_API_ID", "0"))
API_HASH = os.getenv("TG_API_HASH", "")
ASSISTANT_AGENT_HOSTED_ADDRESS = os.getenv("ASSISTANT_AGENT_HOSTED_ADDRESS")

if not API_ID or not API_HASH or not ASSISTANT_AGENT_HOSTED_ADDRESS:
    raise ValueError("Missing TG_API_ID, TG_API_HASH or ASSISTANT_AGENT_HOSTED_ADDRESS in .env")

telegram_client = TelegramClient("userbot_session", API_ID, API_HASH)

userbot_agent = Agent(
    name="userbot_agent",
    seed="userbot-seed",
    port=8005,
    mailbox=True
)

print(f"✅ userbot_agent.address = {userbot_agent.address}")

agent_context: Context = None
last_sender = None
agent_ready = asyncio.Event()
pending_messages = []

async def handle_local_user_input(ctx: Context, sender: str, msg: UserbotInput):
    global agent_context
    agent_context = ctx

    if not agent_ready.is_set():
        agent_ready.set()
        for text, sender_id in pending_messages:
            print(f"📤 Processing queued message: {text}")
            global last_sender_id
            last_sender_id = sender_id
            await handle_local_user_input(ctx, sender, UserbotInput(text=text))
        pending_messages.clear()

    if msg.text.strip().lower() == "summary":
            ctx.logger.info("📝 User triggered summary manually.")
            await ctx.send(ASSISTANT_AGENT_HOSTED_ADDRESS, SummaryTrigger())
            return

    ctx.logger.info(f"[userbot] Forwarding to Assistant: {msg.text}")
    await ctx.send(
        ASSISTANT_AGENT_HOSTED_ADDRESS,
        AssistantInput(
            user_message=msg.text,
            reply_to=userbot_agent.address
        )
    )

@userbot_agent.on_message(model=AssistantOutput)
async def handle_assistant_reply(ctx: Context, sender: str, msg: AssistantOutput):
    global last_sender
    if last_sender:
        await telegram_client.send_message(last_sender, msg.agent_reply)
        ctx.logger.info(f"📤 Sent to Telegram: {msg.agent_reply}")

        if msg.summary and msg.summary != "...":
            me = await telegram_client.get_me()
            sender = await telegram_client.get_entity(last_sender)
            summary_message = f"📌 *Summary of your chat with {getattr(sender, 'first_name', 'unknown')}*: \n{msg.summary}"
            await telegram_client.send_message(me.id, summary_message)
            ctx.logger.info(f"📌 Sent summary to self: {msg.summary}")

@telegram_client.on(events.NewMessage)
async def on_new_message(event):
    global agent_context, last_sender

    text = event.message.message
    sender = await event.get_input_sender()
    last_sender = sender
    print(f"[TELEGRAM] Incoming msg from {sender}: {text}")

    me = await telegram_client.get_me()
    sender_id = event.sender_id

    if text.strip().lower() == "/summary" and sender_id == me.id:
        print("📝 Summary manually triggered by the user.")
        await handle_local_user_input(agent_context, userbot_agent.address, UserbotInput(text="summary"))
        return
    
    if not event.is_private or sender_id == me.id:
        return

    if not agent_ready.is_set():
        print("⏳ Agent not ready. Queuing message.")
        pending_messages.append((text, last_sender))
        return

    await handle_local_user_input(agent_context, userbot_agent.address, UserbotInput(text=text))

@userbot_agent.on_interval(period=2.0)
async def setup_context(ctx: Context):
    global agent_context
    if not agent_context:
        print("✅ Agent context initialized.")
        agent_context = ctx
        agent_ready.set()

async def main():
    print("🚀 Starting userbot and agent...")
    await asyncio.gather(
        userbot_agent.run_async(),
        telegram_client.start(),
        telegram_client.run_until_disconnected()
    )

if __name__ == "__main__":
    with telegram_client:
        telegram_client.loop.run_until_complete(main())
