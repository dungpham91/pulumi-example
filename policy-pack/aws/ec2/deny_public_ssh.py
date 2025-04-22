from pulumi_policy import (
    ReportViolation,
    ResourceValidationArgs,
    ResourceValidationPolicy,
)

def ec2_deny_public_ssh_validator(args: ResourceValidationArgs, report_violation: ReportViolation):
    if args.resource_type == "aws:ec2/securityGroup:SecurityGroup":
        ingress_rules = args.props.get("ingress", [])
        for rule in ingress_rules:
            cidrs = rule.get("cidrBlocks", [])
            from_port = rule.get("fromPort")
            to_port = rule.get("toPort")
            if "0.0.0.0/0" in cidrs and (from_port == 22 or to_port == 22):
                report_violation(
                    "EC2 Security Group should not allow SSH (port 22) access from the entire internet (0.0.0.0/0). " +
                    "Consider restricting the source IP range for enhanced security.")

ec2_deny_public_ssh = ResourceValidationPolicy(
    name="ec2-deny-public-ssh",
    description="Prohibits EC2 Security Groups from allowing SSH access from the entire internet.",
    validate=ec2_deny_public_ssh_validator,
)