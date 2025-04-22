# infra/modules/security_group.py
import pulumi
import pulumi_aws as aws
import config

def create_web_security_group(name: str, vpc_id: pulumi.Input[str]):
    """
    Creates a Security Group for the Web Server:
    - Allows inbound HTTP (80) and HTTPS (443) from anywhere.
    - Allows inbound SSH (22) only from the configured IP.
    - Allows all outbound traffic (default).
    """
    sg = aws.ec2.SecurityGroup(name,
        vpc_id=vpc_id,
        description="Allow HTTP, HTTPS inbound traffic and SSH from specific IP",
        tags={**config.common_tags, "Name": f"{name}-sg"},
        ingress=[
            aws.ec2.SecurityGroupIngressArgs(
                protocol="tcp",
                from_port=80,
                to_port=80,
                cidr_blocks=["0.0.0.0/0"],
                description="Allow HTTP traffic",
            ),
            aws.ec2.SecurityGroupIngressArgs(
                protocol="tcp",
                from_port=443,
                to_port=443,
                cidr_blocks=["0.0.0.0/0"],
                description="Allow HTTPS traffic",
            ),
            aws.ec2.SecurityGroupIngressArgs(
                # Create a for port 8080 to test policy pack
                # This rule should be blocked by the policy pack
                protocol="tcp",
                from_port=8080,
                to_port=8080,
                cidr_blocks=["0.0.0.0/0"],
                description="Allow 8080 traffic",
            ),
            aws.ec2.SecurityGroupIngressArgs(
                # Allow SSH from internet to test policy pack
                # This rule should be blocked by the policy pack
                protocol="tcp",
                from_port=22,
                to_port=22,
                cidr_blocks=["0.0.0.0/0"],
                #cidr_blocks=[f"{config.allowed_ssh_ip}/32"], # Only allow from configured IP
                description="Allow SSH traffic from specific IP",
            ),
        ],
        egress=[
            aws.ec2.SecurityGroupEgressArgs(
                protocol="-1", # -1 means all protocols
                from_port=0,
                to_port=0,
                cidr_blocks=["0.0.0.0/0"],
                description="Allow all outbound traffic",
            ),
        ]
    )
    return sg
