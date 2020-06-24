import discord

from aws import AWSService
from constants import AUTHORIZED_CHANNEL, AUTHORIZED_ROLE
from mc import MCRconService


class ChatService:
    def __init__(self):
        self.aws_service = AWSService()
        self.server_state = None
        self.server_ip = None
        self.is_server_started = None
        self.is_server_stopped = None
        self.number_of_users = 0
        self.max_users = 0
        self.users = []

    def filter_message(
        self, message: discord.message.Message, client: discord.client.Client
    ) -> bool:
        if message.author == client.user:
            return True

        if AUTHORIZED_CHANNEL != message.channel.name:
            return True

        user_role_names = [role.name for role in message.author.roles]

        if AUTHORIZED_ROLE not in user_role_names:
            return True

        if not message.content.startswith("!mc "):
            return True

    def handle_message(self, message: discord.message.Message) -> str:
        message_params = message.content.split(" ")[1:]
        number_of_arguments = len(message_params)

        if number_of_arguments == 2:
            if message_params[0] == "server" and message_params[1] == "status":
                return self.server_status()
            elif message_params[0] == "server" and message_params[1] == "start":
                return self.server_start()
            elif message_params[0] == "server" and message_params[1] == "stop":
                return self.server_stop_check()
        elif number_of_arguments == 3:
            if (
                message_params[0] == "server"
                and message_params[1] == "stop"
                and message_params[2] == "force"
            ):
                return self.server_stop()

        return self.help_message()

    def parse_server_status(self, server_status: dict):
        self.server_state = server_status.get("state")
        self.server_ip = server_status.get("ip")
        self.is_server_started = server_status.get("start")
        self.is_server_stopped = server_status.get("stop")

    def parse_user_list(self):
        try:
            mcr = MCRconService(self.server_ip)
            mcr.parse_user_list(mcr.list_users())
            self.number_of_users = mcr.number_of_users
            self.max_users = mcr.max_users
            self.users = mcr.users
        except ConnectionRefusedError as e:
            print(e)

    def server_status(self) -> str:
        self.parse_server_status(self.aws_service.check_server_status())
        message = f"Server status:\n" f"\t VM State: {self.server_state}\n"
        if self.server_ip:
            self.parse_user_list()
            message += f"\t IP: {self.server_ip}:25565\n"
            message += f"\t Users: {self.number_of_users}/{self.max_users} online\n"
            if self.number_of_users:
                for user in self.users:
                    message += f"\t\t - {user}\n"

        return message

    def server_start(self) -> str:
        self.parse_server_status(self.aws_service.start_server())
        if self.is_server_started:
            return (
                f"Server Running:\n"
                f"\t VM State: {self.server_state}\n"
                f"\t IP: {self.server_ip}:25565\n"
            )
        else:
            return (
                f"Server already running:\n"
                f"\t VM State: {self.server_state}\n"
                f"\t IP: {self.server_ip}:25565\n"
            )

    def server_stop_check(self) -> str:
        self.parse_server_status(self.aws_service.check_server_status())
        if not self.server_ip:
            return f"Server already stopped:\n" f"\t State: {self.server_state}\n"
        self.parse_user_list()
        if self.number_of_users:
            return f"There are {self.number_of_users} user(s) online, are you sure?"
        else:
            return self.server_stop()

    def server_stop(self) -> str:
        self.parse_server_status(self.aws_service.stop_server())
        if self.is_server_stopped:
            return f"Server stopping:\n" f"\t State: {self.server_state}\n"
        else:
            return f"Server already stopped:\n" f"\t State: {self.server_state}\n"

    def help_message(self) -> str:
        return (
            "Available Commands:\n"
            "\t- !mc server status\n"
            "\t- !mc server start\n"
            "\t- !mc server stop\n"
            "\t- !mc server stop force\n"
        )
