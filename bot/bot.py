import asyncio

import discord

from chat import ChatService
from constants import DISCORD_BOT_TOKEN, MC_CHANNEL_ID, SERVER_CHECK_INTERVAL
from mc_server_status import MCServerStatus


class BotClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.mcss = MCServerStatus()
        self.chat_service = ChatService()
        self.bg_task = self.loop.create_task(self.background_task())

    async def on_ready(self):
        print(f"We have logged in as {client.user}")

    async def on_message(self, message: discord.message.Message):
        if self.chat_service.filter_message(message, client):
            return

        await message.channel.send(self.chat_service.handle_message(message))

    async def background_task(self):
        await self.wait_until_ready()

        channel = self.get_channel(MC_CHANNEL_ID)
        while not self.is_closed():
            if self.mcss.mc_server_status():
                await channel.send("Server inactive, shutting down")
            await asyncio.sleep(SERVER_CHECK_INTERVAL)


client = BotClient()
client.run(DISCORD_BOT_TOKEN)
