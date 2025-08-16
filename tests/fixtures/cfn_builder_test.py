# CloudFormation builder test implementation
from troposphere import s3

from helpers.cfn_builder import CfnBuilder


class TestCfnBuilder(CfnBuilder):
    """Simple test builder for CfnBuilder testing."""

    def _build(self, cfn_template, params):
        """Test implementation that adds an S3 bucket."""
        bucket = s3.Bucket(
            "TestBucket", BucketName=params.get("bucket_name", "test-bucket")
        )
        cfn_template.add_resource(bucket)
        return None  # Use existing template
