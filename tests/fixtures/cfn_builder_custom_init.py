# CloudFormation builder with custom initialization
from troposphere import Parameter, Template, s3

from helpers.cfn_builder import CfnBuilder


class TestCfnBuilderCustomInit(CfnBuilder):
    """Test builder with custom initialization."""

    def _init(self, params, description):
        """Custom initialization that adds parameters."""
        cfn_template = Template()
        cfn_template.set_version()
        if description:
            cfn_template.set_description(description)

        # Add custom parameter
        bucket_param = Parameter(
            "BucketName",
            Type="String",
            Description="Name of the S3 bucket",
            Default=params.get("bucket_name", "default-bucket"),
        )
        cfn_template.add_parameter(bucket_param)
        return cfn_template

    def _build(self, cfn_template, params):
        """Test implementation using custom template."""
        bucket = s3.Bucket("CustomInitBucket", BucketName={"Ref": "BucketName"})
        cfn_template.add_resource(bucket)
