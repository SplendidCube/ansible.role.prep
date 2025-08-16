# Test AWS resource model implementation
from helpers.aws_resource_model import AwsResourceModel


class TestAwsModel(AwsResourceModel):
    """Simple test model for AwsResourceModel testing."""

    def run(self, params, response):
        """Test implementation that modifies response directly."""
        response["Resources"] = {
            "TestResource": {
                "Type": "AWS::S3::Bucket",
                "Properties": {"BucketName": params.get("bucket_name", "test-bucket")},
            }
        }
        return {"Status": "Created"}
