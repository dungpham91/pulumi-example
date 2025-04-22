from pulumi_policy import (
    ReportViolation,
    ResourceValidationArgs,
    ResourceValidationPolicy,
)

ALLOWED_PORTS = [80, 443]

def ec2_restrict_ingress_ports_validator(args: ResourceValidationArgs, report_violation: ReportViolation):
    if args.resource_type == "aws:ec2/securityGroup:SecurityGroup":
        ingress_rules = args.props.get("ingress", [])
        for rule in ingress_rules:
            cidrs = rule.get("cidrBlocks", [])
            from_port = rule.get("fromPort")
            to_port = rule.get("toPort")
            if "0.0.0.0/0" in cidrs:
                if from_port not in ALLOWED_PORTS or to_port not in ALLOWED_PORTS:
                    report_violation(
                        f"EC2 Security Group allows internet access (0.0.0.0/0) to port {int(from_port)}, which includes disallowed ports. " +
                        f"Only ports {ALLOWED_PORTS} are permitted for internet access.")

ec2_restrict_ingress_ports = ResourceValidationPolicy(
    name="ec2-restrict-ingress-ports",
    description="Restricts EC2 Security Groups allowing internet access to only ports 80 and 443.",
    validate=ec2_restrict_ingress_ports_validator,
)
