from mcrcon import MCRcon

from constants import RCON_PASSWORD


class MCRconService:
    def __init__(self, server_ip: str):
        self.mcr = MCRcon(server_ip, RCON_PASSWORD)
        self.mcr.connect()
        self.number_of_users = 0
        self.max_users = 0
        self.users = []

    def __del__(self):
        self.mcr.disconnect()

    def parse_user_list(self, mcr_user_list: str):
        mcr_user_list_split = mcr_user_list.split(": ")
        players_online = mcr_user_list_split[0].split(" ")
        self.number_of_users = int(players_online[2])
        self.max_users = int(players_online[7])
        self.users = mcr_user_list_split[1].split(" ")

    def list_users(self) -> str:
        return self.mcr.command("/list")
