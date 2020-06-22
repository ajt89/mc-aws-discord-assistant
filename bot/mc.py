from mcrcon import MCRcon

from constants import RCON_PASSWORD


class MCRconService:
    def __init__(self, server_ip):
        self.mcr = MCRcon(server_ip, RCON_PASSWORD)
        self.mcr.connect()

    def __del__(self):
        self.mcr.disconnect()

    def list_users(self) -> str:
        return self.mcr.command("/list")
