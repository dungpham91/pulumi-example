import pulumi
import pulumi_aws as aws
from config import config

class StateBackend(pulumi.ComponentResource):
    def __init__(self, name: str, opts: pulumi.ResourceOptions = None):
        super().__init__(f"backend-setup:modules:{name}", name, None, opts)

        # Create S3 bucket to store state
        # S3 bucket will be created with unique name based on stack name and environment
        self.state_bucket = aws.s3.Bucket(f"{name}-bucket",
            bucket=config.state_bucket_name,
            force_destroy=True,
            acl="private",
            versioning=aws.s3.BucketVersioningArgs(
                enabled=True,
            ),
            server_side_encryption_configuration=aws.s3.BucketServerSideEncryptionConfigurationArgs(
                rule=aws.s3.BucketServerSideEncryptionConfigurationRuleArgs(
                    apply_server_side_encryption_by_default=aws.s3.BucketServerSideEncryptionConfigurationRuleApplyServerSideEncryptionByDefaultArgs(
                        sse_algorithm="AES256",
                    ),
                ),
            ),
            tags={
                "Environment": config.environment.capitalize(),
                "Project": "PulumiStateBackend",
                "Name": f"{name}-bucket",
            },
            opts=pulumi.ResourceOptions(parent=self))

        # Create DynamoDB table to lock state
        self.state_lock_table = aws.dynamodb.Table(f"{name}-table",
            name=config.state_lock_table_name,
            attributes=[aws.dynamodb.TableAttributeArgs(
                name="LockID",
                type="S",
            )],
            hash_key="LockID",
            billing_mode="PAY_PER_REQUEST",
            tags={
                "Environment": config.environment.capitalize(),
                "Project": "PulumiStateBackend",
                "Name": f"{name}-table",
            },
            opts=pulumi.ResourceOptions(parent=self))

        # Export important properties
        self.bucket_name = self.state_bucket.bucket
        self.table_name = self.state_lock_table.name

        self.register_outputs({
            "bucket_id": self.bucket_name,
            "table_name": self.table_name,
        })
