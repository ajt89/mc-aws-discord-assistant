import discord

from constants import AUTHORIZED_CHANNEL, AUTHORIZED_ROLE


def filter_message(message: discord.message.Message, client: discord.client.Client) -> bool:
    """
    See if message is from the correct channel and user has correct role
    """
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

    return help_message()


def help_message() -> str:
    return (
        "Available Commands:\n"
        "\t- !mc server status\n"
        "\t- !mc server start\n"
        "\t- !mc server stop\n"
    )
