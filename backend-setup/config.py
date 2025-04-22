import pulumi

class Config:
    def __init__(self):
        self.pulumi_config = pulumi.Config()
        self.aws_region = self.pulumi_config.get("aws:region") or "ap-southeast-1"

        self.environment = pulumi.get_stack() # Get stack name as environment

        if self.environment == "dev":
            self.state_bucket_name = f"devopslite-dev-infra-state-bucket"
            self.state_lock_table_name = f"devopslite-dev-pulumi-state-lock"
        elif self.environment == "prod":
            self.state_bucket_name = f"devopslite-prod-infra-state-bucket"
            self.state_lock_table_name = f"devopslite-prod-pulumi-state-lock"
        else:
            raise ValueError(f"Unsupported environment: {self.environment}")

config = Config()
