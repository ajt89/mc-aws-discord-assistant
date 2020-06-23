from aws import AWSService
from mc import MCRconService


class MCServerStatus:
    def __init__(self):
        self.aws_service = AWSService()
        self.server_state = None
        self.server_ip = None
        self.number_of_users = 0
        self.max_users = 0
        self.users = []

    def parse_user_list(self, server_ip: str):
        try:
            mcr = MCRconService(server_ip)
            mcr.parse_user_list(mcr.list_users())
            self.number_of_users = mcr.number_of_users
            self.max_users = mcr.max_users
            self.users = mcr.users
        except ConnectionRefusedError as e:
            print(e)

    def mc_server_status(self) -> bool:
        # import pdb; pdb.set_trace()
        if not self.aws_service.is_server_running():
            print("Server Offline")
            return False

        self.parse_user_list(self.aws_service.instance_ip)
        if self.number_of_users:
            print("Server Occupied")
            return False

        print("Server Empty, Stopping")
        self.aws_service.stop_server()
        return True
