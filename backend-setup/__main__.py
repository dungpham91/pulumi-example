import pulumi
from modules.state_backend import StateBackend

# Create instance of StateBackend module
state_backend = StateBackend("state-backend")

# Export bucket and table names
pulumi.export("state_bucket_name", state_backend.bucket_name)
pulumi.export("state_lock_table_name", state_backend.table_name)
