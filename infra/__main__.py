# infra/__main__.py
import pulumi
import config # Import shared configuration
from modules import network, security_group, webserver # Import resource modules

# --- 1. Create Network Infrastructure ---
vpc_component = network.create_vpc(f"{config.project_name}-{config.stack_name}")

# --- 2. Create Security Group ---
# Get the VPC ID from the created component
vpc_id = vpc_component.vpc_id

web_sg = security_group.create_web_security_group(
    f"{config.project_name}-websg-{config.stack_name}",
    vpc_id=vpc_id
)

# --- 3. Create Web Server ---
# Select a public subnet from the VPC to place the EC2 instance
# vpc_component.public_subnet_ids is an Output<List<String>>, use .apply for complex logic
# or directly access the first element if sure there's at least one public subnet
public_subnet_id = vpc_component.public_subnet_ids[0]

web_instance, web_eip = webserver.create_web_server(
    f"{config.project_name}-web-{config.stack_name}",
    subnet_id=public_subnet_id,
    security_group_id=web_sg.id
)

# --- 4. Export Important Values ---
pulumi.export("vpc_id", vpc_id)
pulumi.export("public_subnet_ids", vpc_component.public_subnet_ids)
pulumi.export("private_subnet_ids", vpc_component.private_subnet_ids)
pulumi.export("web_security_group_id", web_sg.id)
pulumi.export("web_instance_id", web_instance.id)
pulumi.export("web_server_public_ip", web_eip.public_ip) # IP to access Nginx
pulumi.export("ssh_command", pulumi.Output.concat("ssh ec2-user@", web_eip.public_ip)) # Suggested SSH command
