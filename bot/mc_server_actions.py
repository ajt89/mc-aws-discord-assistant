from aws import AWSService
from mc import MCService


class MCServerActions:
    def __init__(self):
        self.aws_service = AWSService()
        self.mc_service = None
        self._update_or_create_mc_service()

    def _update_or_create_mc_service(self):
        if self.mc_service:
            self.mc_service.update_server_details()
            return

        if self.aws_service.instance_ip:
            self.mc_service = MCService(self.aws_service.instance_ip)

    def shutdown_server(self) -> bool:
        self._update_or_create_mc_service()

        if self.mc_service:
            self.mc_service.stop_server()

        return self.aws_service.stop_instance()

    def shutdown_if_server_inactive(self) -> bool:
        """Check if server is inactive and shutdown

        Returns:
            bool: True if server is inactive and shutdown, False otherwise
        """
        if not self.aws_service.is_instance_running:
            return False

        self._update_or_create_mc_service()

        if self.mc_service.number_of_users:
            return False

        return self.shutdown_server()

    def start_server(self) -> bool:
        """Start server if not running

        Returns:
            bool: True if server was started, False otherwise
        """
        return self.aws_service.start_instance()

    def get_server_status(self) -> dict:
        self.aws_service.update_instance_details()
        self._update_or_create_mc_service()

        aws_instance = {
            "state": self.aws_service.instance_state,
            "ip": self.aws_service.instance_ip,
            "is_running": self.aws_service.is_instance_running,
        }

        mc_server = None
        if self.mc_service:
            mc_server = {
                "is_inactive": bool(self.mc_service.number_of_users),
                "is_server_reachable": bool(self.mc_service.max_users),
                "active_users": self.mc_service.number_of_users,
                "max_users": self.mc_service.max_users,
                "users": self.mc_service.users,
            }

        return {
            "aws_instance": aws_instance,
            "mc_server": mc_server or {},
        }
