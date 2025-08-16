# CloudFormation builder that returns new template
from troposphere import Template, s3

from helpers.cfn_builder import CfnBuilder


class TestCfnBuilderNewTemplate(CfnBuilder):
    """Test builder that returns a new template."""

    def _build(self, cfn_template, params):
        """Test implementation that returns a new template."""
        new_template = Template()
        new_template.set_version()
        new_template.set_description("New template from builder")

        bucket = s3.Bucket(
            "NewTemplateBucket",
            BucketName=params.get("bucket_name", "new-template-bucket"),
        )
        new_template.add_resource(bucket)
        return new_template
