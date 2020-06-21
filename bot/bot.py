import discord

from chat import filter_message, handle_message
from constants import DISCORD_BOT_TOKEN

client = discord.Client()


@client.event
async def on_message(message: discord.message.Message):
    if filter_message(message, client):
        return

    await message.channel.send(handle_message(message))


client.run(DISCORD_BOT_TOKEN)
