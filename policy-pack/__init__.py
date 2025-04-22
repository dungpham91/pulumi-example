from .aws import (
    ec2_deny_public_ssh,
    ec2_restrict_ingress_ports,
)

__all__ = [
    "ec2_deny_public_ssh",
    "ec2_restrict_ingress_ports",
]
