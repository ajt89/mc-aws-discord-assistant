import time

import boto3

from mcad.constants import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, EC2_INSTANCE_NAME, REGION

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
        self.is_instance_running = None

        self._parse_instance_details(self._get_instance_by_name())

    def _get_instance_by_name(self) -> dict:
        response = self.ec2_client.describe_instances(
            Filters=[{"Name": "tag:Name", "Values": [EC2_INSTANCE_NAME]}]
        )
        return response.get("Reservations")[0].get("Instances")[0]

    def _get_instance_by_id(self) -> dict:
        response = self.ec2_client.describe_instances(InstanceIds=[self.instance_id])
        return response.get("Reservations")[0].get("Instances")[0]

    def _parse_instance_details(self, instance: dict):
        self.instance_id = instance.get("InstanceId")
        self.instance_state = instance.get("State").get("Name")
        self.instance_dns = instance.get("PublicDnsName")
        self.instance_ip = instance.get("PublicIpAddress")
        self.is_instance_running = bool(self.instance_state in RUNNING_STATES)

    def update_instance_details(self):
        """Update instance state, dns, ip, and state
        """
        self._parse_instance_details(self._get_instance_by_id())

    def start_instance(self) -> bool:
        """Start the instance if not in running state
        
        Returns:
            bool: True if actions taken, False if no actions are taken
        """
        self.update_instance_details()
        if self.is_instance_running:
            return False

        self.ec2_client.start_instances(InstanceIds=[self.instance_id])
        self.update_instance_details()

        while self.instance_state == "pending":
            time.sleep(5)
            self.update_instance_details()

        self.update_instance_details()
        return True

    def stop_instance(self) -> bool:
        """Stop the instance if not in a stopped state

        Return:
            bool: True if actions taken, False if no actions are taken
        """
        self.update_instance_details()
        if not self.is_instance_running:
            return False

        self.ec2_client.stop_instances(InstanceIds=[self.instance_id])
        self.update_instance_details()
        return True
