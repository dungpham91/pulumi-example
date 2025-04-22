from pulumi_policy import EnforcementLevel, PolicyPack
from aws.ec2.deny_public_ssh import ec2_deny_public_ssh
from aws.ec2.restrict_ingress_ports import ec2_restrict_ingress_ports

PolicyPack(
    name="aws-python",
    enforcement_level=EnforcementLevel.MANDATORY,
    policies=[
        ec2_deny_public_ssh,
        ec2_restrict_ingress_ports,
    ],
)
