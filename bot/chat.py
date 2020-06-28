import discord

from bot.constants import AUTHORIZED_CHANNEL, AUTHORIZED_ROLE
from bot.mc_server_actions import MCServerActions


class ChatService:
    def __init__(self):
        self.mcsa = MCServerActions()

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
                return "Server status:\n" + self._server_status()
            elif message_params[0] == "server" and message_params[1] == "start":
                return self._server_start()
            elif message_params[0] == "server" and message_params[1] == "stop":
                return self._server_stop_check()
        elif number_of_arguments == 3:
            if (
                message_params[0] == "server"
                and message_params[1] == "stop"
                and message_params[2] == "force"
            ):
                return self._server_stop()

        return self._help_message()

    def _server_status(self, is_server_starting=False, is_server_stopping=False) -> str:
        server_status = self.mcsa.get_server_status()
        aws_instance = server_status.get("aws_instance")
        mc_server = server_status.get("mc_server")

        instance_state = aws_instance.get("state")
        is_instance_running = aws_instance.get("is_running")
        instance_ip = aws_instance.get("ip")
        is_server_reachable = mc_server.get("is_server_reachable")
        mc_active_users = mc_server.get("active_users", 0)
        mc_max_users = mc_server.get("max_users", 0)
        mc_users = mc_server.get("users", [])

        message = f"\t Instance State: {instance_state}\n"
        if is_instance_running:
            message += f"\t Server IP: {instance_ip}:25565\n"

        if is_server_stopping:
            message += "\t Server State: stopping\n"
        elif is_server_reachable:
            message += "\t Server State: running\n"
            message += f"\t Users: {mc_active_users}/{mc_max_users} online\n"
            if mc_active_users:
                for user in mc_users:
                    message += f"\t\t - {user}\n"
        elif not is_server_reachable and is_server_starting:
            message += "\t Server State: starting\n"
        elif not is_server_reachable and is_instance_running:
            message += "\n Minecraft Server not reachable!\n"

        return message

    def _server_start(self) -> str:
        message = ""
        if self.mcsa.start_server():
            message = "Instance Starting:\n" + self._server_status(is_server_starting=True)
        else:
            message = "Instance Already Running:\n" + self._server_status(is_server_starting=True)

        return message

    def _server_stop_check(self) -> str:
        message = ""
        if self.mcsa.shutdown_if_server_inactive():
            message = "Server Stopping:\n" + self._server_status(is_server_stopping=True)
        else:
            message = "Server Not Stopped:\n" + self._server_status()

        return message

    def _server_stop(self) -> str:
        message = ""
        if self.mcsa.shutdown_server():
            message = "Server Stopping:\n" + self._server_status(is_server_stopping=True)
        else:
            message = "Server Already Stopped:\n" + self._server_status()

        return message

    def _help_message(self) -> str:
        return (
            "Available Commands:\n"
            "\t- !mc server status\n"
            "\t- !mc server start\n"
            "\t- !mc server stop\n"
            "\t- !mc server stop force\n"
        )
