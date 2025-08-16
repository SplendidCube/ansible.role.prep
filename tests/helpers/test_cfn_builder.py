"""
Comprehensive test suite for helpers.cfn_builder module.

This module provides complete test coverage for the CfnBuilder abstract
base class, including template generation, parameter filtering, initialization,
error handling, and the class counter functionality.
"""

from unittest.mock import Mock

import pytest
from troposphere import Template, s3

from helpers.cfn_builder import CfnBuilder


class ConcreteTestBuilder(CfnBuilder):
    """Concrete test implementation of CfnBuilder for testing."""

    def _build(self, cfn_template, params):
        """Test implementation that adds an S3 bucket."""
        bucket = s3.Bucket(
            "TestBucket", BucketName=params.get("bucket_name", "test-bucket")
        )
        cfn_template.add_resource(bucket)
        return None


class ConcreteTestBuilderNewTemplate(CfnBuilder):
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


class ConcreteTestBuilderCustomFilter(CfnBuilder):
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


class ConcreteTestBuilderCustomInit(CfnBuilder):
    """Test builder with custom initialization."""

    def _init(self, params, description):
        """Custom initialization that adds parameters."""
        from troposphere import Parameter

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
        bucket = s3.Bucket(
            "CustomInitBucket", BucketName=params.get("bucket_name", "default-bucket")
        )
        cfn_template.add_resource(bucket)


class ConcreteTestBuilderError(CfnBuilder):
    """Test builder that raises an exception during build."""

    def _build(self, cfn_template, params):
        """Test implementation that raises an exception."""
        raise RuntimeError("Test error in build method")


def test_cfn_builder_is_abstract():
    """
    Test that CfnBuilder cannot be instantiated directly.

    Verifies that the abstract base class properly prevents direct instantiation
    and requires implementation of abstract methods.
    """
    with pytest.raises(TypeError, match="Can't instantiate abstract class"):
        CfnBuilder()


def test_generate_basic_functionality():
    """
    Test basic generate method functionality.

    Verifies the complete workflow of parameter filtering, template initialization,
    building, and YAML output generation.
    """
    builder = ConcreteTestBuilder()
    mock_ansible = Mock()

    result = builder.generate(
        params={"bucket_name": "test-cfn-bucket"},
        description="Test CloudFormation template",
        ansible=mock_ansible,
    )

    # Verify YAML output structure
    assert "AWSTemplateFormatVersion:" in result
    assert "Description: Test CloudFormation template" in result
    assert "Resources:" in result
    assert "TestBucket:" in result
    assert "AWS::S3::Bucket" in result


def test_generate_with_empty_description():
    """
    Test generate method with empty description.

    Verifies that empty descriptions are handled properly in template initialization.
    """
    builder = ConcreteTestBuilder()
    mock_ansible = Mock()

    result = builder.generate(
        params={"bucket_name": "no-desc-bucket"}, description="", ansible=mock_ansible
    )

    # Should not contain description in output
    assert "AWSTemplateFormatVersion:" in result
    assert "Description:" not in result
    assert "Resources:" in result


def test_generate_with_none_description():
    """
    Test generate method with None description.

    Verifies that None descriptions are handled properly.
    """
    builder = ConcreteTestBuilder()
    mock_ansible = Mock()

    result = builder.generate(
        params={"bucket_name": "none-desc-bucket"},
        description=None,
        ansible=mock_ansible,
    )

    assert "AWSTemplateFormatVersion:" in result
    assert "Description:" not in result


def test_generate_returns_new_template():
    """
    Test generate method when _build returns a new template.

    Verifies that when _build returns a Template object, it replaces
    the original template in the output.
    """
    builder = ConcreteTestBuilderNewTemplate()
    mock_ansible = Mock()

    result = builder.generate(
        params={"bucket_name": "new-template-bucket"},
        description="Original description",
        ansible=mock_ansible,
    )

    # Should use the new template with its own description
    assert "Description: New template from builder" in result
    assert "NewTemplateBucket:" in result
    assert "new-template-bucket" in result


def test_generate_error_handling():
    """
    Test error handling in generate method.

    Verifies that exceptions during template generation are caught
    and properly reported through ansible.fail_json.
    """
    builder = ConcreteTestBuilderError()
    mock_ansible = Mock()

    builder.generate(params={}, description="Error test", ansible=mock_ansible)

    # Verify fail_json was called with proper error information
    mock_ansible.fail_json.assert_called_once()
    call_args = mock_ansible.fail_json.call_args[1]

    assert "msg" in call_args
    assert "CloudFormation template generation failed" in call_args["msg"]
    assert "Test error in build method" in call_args["msg"]
    assert "traceback" in call_args


def test_filter_params_default_behavior():
    """
    Test default parameter filtering behavior.

    Verifies that the default _filter_params method returns parameters unchanged.
    """
    builder = ConcreteTestBuilder()
    test_params = {"bucket_name": "filter-test", "extra_param": "value"}

    filtered = builder._filter_params(test_params)

    assert filtered == test_params


def test_filter_params_custom_behavior():
    """
    Test custom parameter filtering behavior.

    Verifies that custom _filter_params implementations work correctly
    and can validate/transform parameters.
    """
    builder = ConcreteTestBuilderCustomFilter()
    mock_ansible = Mock()

    # Test with valid parameters
    result = builder.generate(
        params={"bucket_name": "filtered-bucket", "extra": "ignored"},
        description="Filter test",
        ansible=mock_ansible,
    )

    assert "FilteredBucket:" in result
    assert "filtered-bucket" in result


def test_filter_params_custom_validation_error():
    """
    Test custom parameter filtering with validation error.

    Verifies that parameter validation errors in _filter_params
    are properly handled by the error handling mechanism.
    """
    builder = ConcreteTestBuilderCustomFilter()
    mock_ansible = Mock()

    # Test with missing required parameter
    builder.generate(
        params={"extra": "value"},  # Missing bucket_name
        description="Validation error test",
        ansible=mock_ansible,
    )

    mock_ansible.fail_json.assert_called_once()
    call_args = mock_ansible.fail_json.call_args[1]
    assert "Missing required parameter: bucket_name" in call_args["msg"]


def test_init_default_behavior():
    """
    Test default template initialization behavior.

    Verifies that _init method properly initializes templates with
    version and description.
    """
    builder = ConcreteTestBuilder()

    # Test with description
    template = builder._init({}, "Test description")

    assert isinstance(template, Template)
    yaml_output = template.to_yaml()
    assert "AWSTemplateFormatVersion:" in yaml_output
    assert "Description: Test description" in yaml_output

    # Test without description
    template_no_desc = builder._init({}, None)
    yaml_no_desc = template_no_desc.to_yaml()
    assert "AWSTemplateFormatVersion:" in yaml_no_desc
    assert "Description:" not in yaml_no_desc


def test_init_custom_behavior():
    """
    Test custom template initialization behavior.

    Verifies that custom _init implementations can add parameters
    and customize template setup.
    """
    builder = ConcreteTestBuilderCustomInit()
    mock_ansible = Mock()

    result = builder.generate(
        params={"bucket_name": "custom-init-bucket"},
        description="Custom init test",
        ansible=mock_ansible,
    )

    # Should include custom parameter
    assert "Parameters:" in result
    assert "BucketName:" in result
    assert "Type: String" in result
    assert "CustomInitBucket:" in result


def test_ansible_instance_assignment():
    """
    Test that ansible module instance is properly assigned.

    Verifies that the AnsibleModule instance is stored for use throughout
    the template generation process.
    """
    builder = ConcreteTestBuilder()
    mock_ansible = Mock()

    builder.generate(
        params={}, description="Ansible assignment test", ansible=mock_ansible
    )

    assert hasattr(builder, "ansible")
    assert builder.ansible is mock_ansible


def test_increment_counter_basic():
    """
    Test basic counter increment functionality.

    Verifies that class-level counter works correctly for unique naming.
    """
    # Reset counter for clean test
    CfnBuilder.counter = 0

    assert CfnBuilder.increment() == 1
    assert CfnBuilder.increment() == 2
    assert CfnBuilder.increment() == 3


def test_increment_counter_custom_start():
    """
    Test counter increment with custom starting value.

    Verifies that counter can be initialized to specific starting values.
    """
    CfnBuilder.counter = 0

    assert CfnBuilder.increment(start=10) == 10
    assert CfnBuilder.increment() == 11
    assert CfnBuilder.increment() == 12


def test_increment_counter_shared_across_instances():
    """
    Test that counter is shared across class instances.

    Verifies that the counter is truly class-level and shared
    between all instances of CfnBuilder subclasses.
    """
    CfnBuilder.counter = 0

    builder1 = ConcreteTestBuilder()
    builder2 = ConcreteTestBuilder()

    # Counter should be shared
    assert builder1.increment() == 1
    assert builder2.increment() == 2
    assert ConcreteTestBuilder.increment() == 3


def test_increment_counter_persistence():
    """
    Test counter persistence across multiple calls.

    Verifies that counter maintains state properly and doesn't reset
    unexpectedly during template generation.
    """
    CfnBuilder.counter = 5

    values = []
    for _ in range(5):
        values.append(CfnBuilder.increment())

    assert values == [6, 7, 8, 9, 10]
    assert CfnBuilder.counter == 10


def test_complete_workflow_integration():
    """
    Test complete workflow integration.

    Verifies that all components work together correctly in a realistic
    template generation scenario.
    """
    builder = ConcreteTestBuilder()
    mock_ansible = Mock()

    # Reset counter for predictable results
    CfnBuilder.counter = 0

    params = {
        "bucket_name": "integration-test-bucket",
        "region": "eu-west-1",
        "extra_param": "should_be_filtered",
    }

    result = builder.generate(
        params=params, description="Integration test template", ansible=mock_ansible
    )

    # Verify complete YAML structure
    lines = result.split("\n")
    yaml_content = "\n".join(line for line in lines if line.strip())

    assert "AWSTemplateFormatVersion:" in yaml_content
    assert "Description: Integration test template" in yaml_content
    assert "Resources:" in yaml_content
    assert "TestBucket:" in yaml_content
    assert "Type: AWS::S3::Bucket" in yaml_content
    assert "integration-test-bucket" in yaml_content

    # Verify ansible instance was set
    assert builder.ansible is mock_ansible

    # Verify no errors occurred
    assert not mock_ansible.fail_json.called
