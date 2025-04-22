# infra/config.py
import pulumi
import pulumi_aws as aws

# Initialize Config object to read configuration from Pulumi.<stack>.yaml
config = pulumi.Config()

# --- Required Configuration ---
# Get the allowed SSH IP address, raises an error if not defined in Pulumi.<stack>.yaml
allowed_ssh_ip = config.require("allowedSshIp")

# --- Optional Configuration with Defaults ---
# Get the instance type, defaults to t3.micro if not set
instance_type = config.get("instanceType") or "t3.micro"
# Get the VPC CIDR block, defaults to 10.0.0.0/16 if not set
vpc_cidr_block = config.get("vpcCidrBlock") or "10.0.0.0/16"
# Get the project name, defaults to "devopslite" if not set
project_name = config.get("projectName") or "devopslite"
# Get environment name, defaults to "dev" if not set
environment_name = config.get("environmentName") or "dev"

# --- Constants or Dynamic Logic ---
# Get the current AWS region from the provider configuration
aws_region = aws.get_region().name
# Get the stack name from the Pulumi CLI context
stack_name = pulumi.get_stack()

# Define standard tags for all resources
common_tags = {
    "Project": project_name,
    "Stack": stack_name,
    "Environment": environment_name,
    "ManagedBy": "Pulumi",
}

# Find the latest Amazon Linux 2 AMI in the current region
latest_ami = aws.ec2.get_ami(
    most_recent=True,
    owners=["amazon"],
    filters=[
        aws.ec2.GetAmiFilterArgs(name="name", values=["amzn2-ami-hvm-*-x86_64-gp2"]),
        aws.ec2.GetAmiFilterArgs(name="virtualization-type", values=["hvm"]),
    ]
)
ami_id = latest_ami.id
