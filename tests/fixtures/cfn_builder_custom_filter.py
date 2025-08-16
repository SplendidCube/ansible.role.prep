# CloudFormation builder with custom parameter filtering
from troposphere import s3

from helpers.cfn_builder import CfnBuilder


class TestCfnBuilderCustomFilter(CfnBuilder):
    """Test builder with custom parameter filtering."""

    def _filter_params(self, params):
        """Custom parameter filtering that validates required fields."""
        filtered = {}
        required_fields = ["bucket_name"]
        for field in required_fields:
            if field not in params:
                raise ValueError(f"Missing required parameter: {field}")
            filtered[field] = params[field]
        return filtered

    def _build(self, cfn_template, params):
        """Test implementation using filtered params."""
        bucket = s3.Bucket("FilteredBucket", BucketName=params["bucket_name"])
        cfn_template.add_resource(bucket)
