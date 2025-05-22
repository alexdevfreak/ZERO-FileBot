from pyrogram import Client, filters
from pyrogram.types import Message
import base64
from config import BOT_TOKEN, LOG_CHANNEL, DATA_CHANNEL

app = Client("filebot", bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message: Message):
    if len(message.command) > 1:
        code = message.command[1]
        try:
            decoded = base64.b64decode(code).decode()
            file_msg = await client.get_messages(DATA_CHANNEL, int(decoded))
            await file_msg.copy(message.chat.id)
        except Exception as e:
            await message.reply("Invalid or expired file link.")
    else:
        await message.reply("I am alive!\nSend /link by replying to a file to get a shareable link.")

@app.on_message(filters.command("alive"))
async def alive(client, message: Message):
    await message.reply("Bot is working perfectly!")

@app.on_message(filters.command("link") & filters.reply)
async def link(client, message: Message):
    reply = message.reply_to_message
    if not (reply.document or reply.video or reply.photo or reply.audio):
        return await message.reply("Reply to a media message to get a link.")
    try:
        sent = await reply.copy(DATA_CHANNEL)
        file_id = str(sent.id)
        encoded = base64.b64encode(file_id.encode()).decode()
        link = f"https://t.me/{(await app.get_me()).username}?start={encoded}"
        await message.reply(f"Here is your link:\n{link}")
    except Exception as e:
        await message.reply("Failed to generate link.")

app.run()
