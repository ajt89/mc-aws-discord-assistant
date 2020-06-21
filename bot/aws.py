import boto3

from constants import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, REGION

STOPPED_STATES = ["stopping", "stopped"]
RUNNING_STATES = ["pending", "running"]


class AWSService:
    def __init__(self):
        self.ec2_client = boto3.client(
            "ec2",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=REGION,
        )
        self.instance_id = None
        self.instance_state = None
        self.instance_dns = None
        self.instance_ip = None

        self.update_instance_details(self.get_instance_by_name())

    def get_instance_by_name(self) -> dict:
        response = self.ec2_client.describe_instances(
            Filters=[{"Name": "tag:Name", "Values": ["minecraft-server"]}]
        )
        return response.get("Reservations")[0].get("Instances")[0]

    def get_instance_by_id(self) -> dict:
        response = self.ec2_client.describe_instances(InstanceIds=[self.instance_id])
        return response.get("Reservations")[0].get("Instances")[0]

    def update_instance_details(self, instance: dict):
        self.instance_id = instance.get("InstanceId")
        self.instance_state = instance.get("State").get("Name")
        self.instance_dns = instance.get("PublicDnsName")
        self.instance_ip = instance.get("PublicIpAddress")

    def check_server_status(self) -> dict:
        self.update_instance_details(self.get_instance_by_id())
        return {"state": self.instance_state, "dns": self.instance_dns, "ip": self.instance_ip}

    def start_server(self) -> dict:
        self.update_instance_details(self.get_instance_by_id())
        if self.instance_state in RUNNING_STATES:
            return self.check_server_status()

        self.ec2_client.start_instances(InstanceIds=[self.instance_id])
        response = self.check_server_status()

        while self.instance_state == "pending":
            response = self.check_server_status()

        response["start"] = True

        return response

    def stop_server(self) -> dict:
        self.update_instance_details(self.get_instance_by_id())
        if self.instance_state in STOPPED_STATES:
            return self.check_server_status()

        self.ec2_client.stop_instances(InstanceIds=[self.instance_id])
        response = self.check_server_status()
        response["stop"] = True

        return response
