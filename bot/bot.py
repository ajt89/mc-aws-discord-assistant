import discord

from chat import ChatService
from constants import DISCORD_BOT_TOKEN

client = discord.Client()
chat_service = ChatService()


@client.event
async def on_message(message: discord.message.Message):
    if chat_service.filter_message(message, client):
        return

    await message.channel.send(chat_service.handle_message(message))


client.run(DISCORD_BOT_TOKEN)
