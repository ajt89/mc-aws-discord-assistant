from mcrcon import MCRcon, socket

from mcad.constants import RCON_PASSWORD

LIST_USERS_COMMAND = "/list"
STOP_SERVER_COMMAND = "/stop"

MAX_USER_POSITION = 7
NUMBER_OF_USERS_POSITION = 2


class MCService:
    def __init__(self, server_ip: str):
        self.server_ip = server_ip
        self.number_of_users = 0
        self.max_users = 0
        self.users = []
        self.update_server_details()

    def update_server_details(self):
        self._parse_user_list(self._execute_command(LIST_USERS_COMMAND))

    def stop_server(self):
        self._execute_command(STOP_SERVER_COMMAND)

    def _parse_user_list(self, user_list: str):
        if not user_list:
            return

        user_list_split = user_list.split(": ")
        players_online = user_list_split[0].split(" ")
        self.number_of_users = int(players_online[NUMBER_OF_USERS_POSITION])
        self.is_server_active = bool(self.number_of_users)
        self.max_users = int(players_online[MAX_USER_POSITION])
        self.users = user_list_split[1].split(" ")

    def _execute_command(self, command_input: str) -> str:
        command_output = ""
        try:
            with MCRcon(self.server_ip, RCON_PASSWORD) as mcr:
                command_output = mcr.command(command_input)
        except Exception as e:
            print(e)

        return command_output
