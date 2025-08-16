# Test AWS resource model that returns None
from helpers.aws_resource_model import AwsResourceModel


class TestAwsModelNoReturn(AwsResourceModel):
    """Test model that modifies response directly and returns None."""

    def run(self, params, response):
        """Test implementation that only modifies response."""
        response["Outputs"] = {
            "ResourceArn": {
                "Description": "ARN of created resource",
                "Value": {"Fn::GetAtt": ["TestResource", "Arn"]},
            }
        }
