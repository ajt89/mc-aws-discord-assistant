import discord

from constants import AUTHORIZED_CHANNEL, AUTHORIZED_ROLE


def filter_message(message: discord.message.Message, client: discord.client.Client) -> bool:
    if message.author == client.user:
        return True

    if AUTHORIZED_CHANNEL != message.channel.name:
        return True

    user_role_names = [role.name for role in message.author.roles]

    if AUTHORIZED_ROLE not in user_role_names:
        return True

    if not message.content.startswith("!mc "):
        return True


def handle_message(message: discord.message.Message) -> str:
    message_params = message.content.split(" ")[1:]

    if message_params[0] == "server" and message_params[1] == "status":
        return server_status()

    return help_message()


def server_status() -> str:
    state = "stopped"
    dns = ""
    return (
        f"Server status:\n"
        f"\t State: {state}\n"
        f"\t DNS: {dns}\n"
    )

def help_message() -> str:
    return (
        "Available Commands:\n"
        "\t- !mc server status\n"
        "\t- !mc server start\n"
        "\t- !mc server stop\n"
    )
