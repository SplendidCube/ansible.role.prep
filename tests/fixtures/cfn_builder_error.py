# CloudFormation builder that raises an exception
from helpers.cfn_builder import CfnBuilder


class TestCfnBuilderError(CfnBuilder):
    """Test builder that raises an exception during build."""

    def _build(self, cfn_template, params):
        """Test implementation that raises an exception."""
        raise RuntimeError("Test error in build method")
