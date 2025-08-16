"""
Comprehensive test suite for helpers.aws_resource_model module.

This module provides complete test coverage for the AwsResourceModel abstract
base class, including parameter processing, model execution, response formatting,
and edge cases.
"""

from unittest.mock import Mock

import pytest
import yaml

from helpers.aws_resource_model import AwsResourceModel


class ConcreteTestModel(AwsResourceModel):
    """Concrete test implementation of AwsResourceModel for testing."""

    def __init__(self, return_data=None):
        self.return_data = return_data or {"Status": "Created"}

    def run(self, params, response):
        """Test implementation that modifies response directly."""
        response["Resources"] = {
            "TestResource": {
                "Type": "AWS::S3::Bucket",
                "Properties": {"BucketName": params.get("bucket_name", "test-bucket")},
            }
        }
        return self.return_data


class ConcreteTestModelNoReturn(AwsResourceModel):
    """Test model that modifies response directly and returns None."""

    def run(self, params, response):
        """Test implementation that only modifies response."""
        response["Outputs"] = {
            "ResourceArn": {
                "Description": "ARN of created resource",
                "Value": {"Fn::GetAtt": ["TestResource", "Arn"]},
            }
        }
        return None


def test_aws_resource_model_is_abstract():
    """
    Test that AwsResourceModel cannot be instantiated directly.

    Verifies that the abstract base class properly prevents direct instantiation
    and requires implementation of abstract methods.
    """
    with pytest.raises(TypeError, match="Can't instantiate abstract class"):
        AwsResourceModel()


def test_generate_basic_functionality():
    """
    Test basic generate method functionality with minimal parameters.

    Verifies the standard workflow of parameter processing, model execution,
    and YAML response formatting.
    """
    model = ConcreteTestModel()
    mock_ansible = Mock()

    result = model.generate(params={"bucket_name": "test-bucket"}, ansible=mock_ansible)

    # Verify YAML output
    parsed = yaml.safe_load(result)
    assert "Resources" in parsed
    assert "Status" in parsed
    assert parsed["Status"] == "Created"
    assert parsed["Resources"]["TestResource"]["Type"] == "AWS::S3::Bucket"
    assert (
        parsed["Resources"]["TestResource"]["Properties"]["BucketName"] == "test-bucket"
    )


def test_generate_with_description():
    """
    Test generate method with description parameter.

    Verifies that optional description is properly included in the response.
    """
    model = ConcreteTestModel()
    mock_ansible = Mock()

    result = model.generate(
        params={"bucket_name": "described-bucket"},
        ansible=mock_ansible,
        description="Test CloudFormation template",
    )

    parsed = yaml.safe_load(result)
    assert "Description" in parsed
    assert parsed["Description"] == "Test CloudFormation template"
    assert "Resources" in parsed
    assert "Status" in parsed


def test_generate_without_description():
    """
    Test generate method without description parameter.

    Verifies that response works correctly when description is None or empty.
    """
    model = ConcreteTestModel()
    mock_ansible = Mock()

    result = model.generate(
        params={"bucket_name": "no-desc-bucket"}, ansible=mock_ansible
    )

    parsed = yaml.safe_load(result)
    assert "Description" not in parsed
    assert "Resources" in parsed
    assert "Status" in parsed


def test_generate_with_empty_description():
    """
    Test generate method with empty string description.

    Verifies that empty string description is treated as falsy and not included.
    """
    model = ConcreteTestModel()
    mock_ansible = Mock()

    result = model.generate(
        params={"bucket_name": "empty-desc-bucket"},
        ansible=mock_ansible,
        description="",
    )

    parsed = yaml.safe_load(result)
    assert "Description" not in parsed
    assert "Resources" in parsed


def test_generate_model_returns_none():
    """
    Test generate method when run() returns None.

    Verifies that the response dictionary can be modified directly
    and None return values are handled properly.
    """
    model = ConcreteTestModelNoReturn()
    mock_ansible = Mock()

    result = model.generate(params={}, ansible=mock_ansible)

    parsed = yaml.safe_load(result)
    assert "Outputs" in parsed
    assert "ResourceArn" in parsed["Outputs"]
    assert parsed["Outputs"]["ResourceArn"]["Description"] == "ARN of created resource"


def test_generate_empty_params():
    """
    Test generate method with empty parameters dictionary.

    Verifies that empty parameters are handled gracefully.
    """
    model = ConcreteTestModel()
    mock_ansible = Mock()

    result = model.generate(params={}, ansible=mock_ansible)

    parsed = yaml.safe_load(result)
    assert "Resources" in parsed
    # Should use default bucket name
    assert (
        parsed["Resources"]["TestResource"]["Properties"]["BucketName"] == "test-bucket"
    )


def test_ansible_instance_assignment():
    """
    Test that ansible module instance is properly assigned to model.

    Verifies that the AnsibleModule instance is stored for use in model methods.
    """
    model = ConcreteTestModel()
    mock_ansible = Mock()

    model.generate(params={}, ansible=mock_ansible)

    # Verify ansible instance was assigned
    assert hasattr(model, "ansible")
    assert model.ansible is mock_ansible


def test_yaml_output_format():
    """
    Test that output is properly formatted as YAML.

    Verifies YAML structure, formatting, and parsing consistency.
    """
    model = ConcreteTestModel()
    mock_ansible = Mock()

    result = model.generate(
        params={"bucket_name": "yaml-test"},
        ansible=mock_ansible,
        description="YAML formatting test",
    )

    # Verify it's valid YAML
    parsed = yaml.safe_load(result)
    assert isinstance(parsed, dict)

    # Verify default_flow_style=False (block style)
    assert "\n" in result  # Should have line breaks
    assert result.strip().endswith("Created")  # Should end with value, not bracket


def test_response_update_merging():
    """
    Test that response updates are properly merged.

    Verifies that dictionary returned by run() method is correctly
    merged with the base response dictionary.
    """
    model = ConcreteTestModel()
    mock_ansible = Mock()

    result = model.generate(
        params={"bucket_name": "merge-test"},
        ansible=mock_ansible,
        description="Merge test",
    )

    parsed = yaml.safe_load(result)

    # Should have both description (from base) and Status (from run() return)
    assert "Description" in parsed
    assert "Status" in parsed
    assert "Resources" in parsed  # From response modification in run()

    assert parsed["Description"] == "Merge test"
    assert parsed["Status"] == "Created"


def test_custom_return_data():
    """
    Test that custom return data from run() method is properly merged.

    Verifies that models can return additional response data that gets merged.
    """
    custom_data = {"Status": "Updated", "Extra": "CustomValue"}
    model = ConcreteTestModel(return_data=custom_data)
    mock_ansible = Mock()

    result = model.generate(
        params={"bucket_name": "custom-test"},
        ansible=mock_ansible,
        description="Custom return data test",
    )

    parsed = yaml.safe_load(result)

    # Should have all merged data
    assert parsed["Status"] == "Updated"
    assert parsed["Extra"] == "CustomValue"
    assert "Description" in parsed
    assert "Resources" in parsed
