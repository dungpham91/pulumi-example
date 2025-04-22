# infra/modules/webserver.py
import pulumi
import pulumi_aws as aws
import config

# Script to run on EC2 instance startup (User Data)
nginx_install_script = """#!/bin/bash
sudo yum update -y
sudo amazon-linux-extras install nginx1 -y
sudo systemctl enable nginx
sudo systemctl start nginx
echo "<h1>Hello from Pulumi and Nginx on EC2! - devopslite.com</h1>" | sudo tee /usr/share/nginx/html/index.html
"""

def create_web_server(
        name: str,
        subnet_id: pulumi.Input[str], # Needs a public subnet for EIP to work
        security_group_id: pulumi.Input[str]):
    """
    Creates an EC2 Instance, installs Nginx, creates an EIP, and associates it with the instance.
    """
    # Create EC2 Instance
    instance = aws.ec2.Instance(name,
        instance_type=config.instance_type,
        vpc_security_group_ids=[security_group_id],
        ami=config.ami_id, # Use the AMI found in config.py
        subnet_id=subnet_id, # Must be a public subnet
        user_data=nginx_install_script, # Nginx installation script
        tags={**config.common_tags, "Name": f"{name}-instance"},
        # associate_public_ip_address=True, # Not needed if using EIP
    )

    # Create Elastic IP (EIP)
    eip = aws.ec2.Eip(f"{name}-eip",
        # instance=instance.id, # Older way of association, EipAssociation is preferred
        domain="vpc", # Specify EIP is for use in VPC
        tags={**config.common_tags, "Name": f"{name}-eip"},
    )

    # Associate EIP with EC2 Instance
    eip_assoc = aws.ec2.EipAssociation(f"{name}-eip-assoc",
        instance_id=instance.id,
        allocation_id=eip.id, # Use allocation_id for VPC EIPs
    )

    return instance, eip
