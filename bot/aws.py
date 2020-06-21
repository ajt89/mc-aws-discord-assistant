import boto3

from constants import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, REGION


class AWSService:
    def __init__(self):
        self.ec2_client = boto3.client(
            "ec2",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=REGION,
        )

    def check_server_status(self) -> dict:
        response = self.ec2_client.describe_instances(
            Filters=[{"Name": "tag:Name", "Values": ["minecraft-server"]}]
        )
        instance = response.get("Reservations")[0].get("Instances")[0]

        return {"state": instance.get("State").get("Name"), "dns": instance.get("PublicDnsName")}
