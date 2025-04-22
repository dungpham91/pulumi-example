# infra/modules/network.py
import pulumi
import pulumi_awsx as awsx # Use awsx for simplified VPC creation
import config # Import the config module to get tags and cidr

def create_vpc(name: str):
    """
    Creates a VPC with 2 public and 2 private subnets spanning 2 AZs.
    Uses pulumi_awsx to simplify the creation of Subnets, Route Tables, IGW, NAT Gateway (awsx creates NAT by default).
    """
    vpc = awsx.ec2.Vpc(name,
        cidr_block=config.vpc_cidr_block,
        # Use 1 AZ to test policy pack
        number_of_availability_zones=1,
        # Add explicit subnet strategy
        subnet_strategy=awsx.ec2.SubnetAllocationStrategy.AUTO,
        subnet_specs=[
            awsx.ec2.SubnetSpecArgs(
                type=awsx.ec2.SubnetType.PRIVATE,
                name="private",
                cidr_mask=24  # Specify CIDR mask for private subnets
            ),
            awsx.ec2.SubnetSpecArgs(
                type=awsx.ec2.SubnetType.PUBLIC,
                name="public",
                cidr_mask=24  # Specify CIDR mask for public subnets
            ),
        ],
        tags={**config.common_tags, "Name": f"{name}-vpc"},
        enable_dns_hostnames=True, # Enable DNS hostnames for the VPC
        nat_gateways=awsx.ec2.NatGatewayConfigurationArgs(strategy=awsx.ec2.NatGatewayStrategy.SINGLE), # Configure NAT Gateways
    )
    return vpc
