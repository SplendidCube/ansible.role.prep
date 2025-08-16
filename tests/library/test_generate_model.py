"""
Comprehensive tests for the generate_model Ansible module.

This test suite provides extensive coverage of all functions and edge cases
in the generate_model module, following pytest best practices and the
established code quality standards.
"""

import os
from pathlib import Path
from typing import Any
from unittest.mock import Mock, patch

import pytest
import stringcase
from generate_model import get_module_path, get_path, main, run_module


# Local MockModel class for type annotations
# The actual MockModel fixture is in conftest.py
class MockModel:
    """Mock model class for testing module execution."""

    def __init__(self, return_value: Any = "test output"):
        self.return_value = return_value
        self.generate_called = False
        self.generate_args = None
        self.generate_kwargs = None

    def generate(self, params: dict[str, Any], description: str, ansible: Any) -> Any:
        self.generate_called = True
        self.generate_args = (params, description, ansible)
        self.generate_kwargs = {
            "params": params,
            "description": description,
            "ansible": ansible,
        }
        return self.return_value


# Tests for get_path function
def test_get_path_with_valid_existing_file(tmp_path: Path) -> None:
    """
    Test get_path returns correct absolute path for existing Python file.

    :param tmp_path: Pytest temporary directory fixture
    :type tmp_path: Path
    """
    # Create a temporary Python file
    test_file = tmp_path / "test_module.py"
    test_file.write_text("# Test module")

    # Get the path without extension
    model_path = str(test_file)[:-3]  # Remove .py
    result = get_path(model_path)

    assert isinstance(result, str)
    assert result == model_path
    assert not result.endswith(".py")
    assert os.path.isabs(result)


def test_get_path_with_nonexistent_file() -> None:
    """
    Test get_path raises FileNotFoundError for non-existent files.
    """
    with pytest.raises(FileNotFoundError, match="Model file .* not found"):
        get_path("some/completely/fake/location")


def test_get_path_with_empty_string() -> None:
    """
    Test get_path raises ValueError for empty model path.
    """
    with pytest.raises(ValueError, match="Model path must be a non-empty string"):
        get_path("")


def test_get_path_with_none_input() -> None:
    """
    Test get_path raises ValueError for None input.
    """
    with pytest.raises(ValueError, match="Model path must be a non-empty string"):
        get_path(None)


def test_get_path_with_non_string_input() -> None:
    """
    Test get_path raises ValueError for non-string input.
    """
    with pytest.raises(ValueError, match="Model path must be a non-empty string"):
        get_path(123)


def test_get_path_with_relative_path(tmp_path: Path) -> None:
    """
    Test get_path works with relative paths and converts to absolute.

    :param tmp_path: Pytest temporary directory fixture
    :type tmp_path: Path
    """
    # Create a test file in a subdirectory
    subdir = tmp_path / "models"
    subdir.mkdir()
    test_file = subdir / "relative_test.py"
    test_file.write_text("# Relative test module")

    # Change to the parent directory and test with relative path
    original_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        result = get_path("models/relative_test")
        assert os.path.isabs(result)
        assert result.endswith("models/relative_test")
        assert not result.endswith(".py")
    finally:
        os.chdir(original_cwd)


def test_get_path_with_windows_backslashes(tmp_path: Path) -> None:
    """
    Test get_path handles Windows-style backslash paths correctly.

    :param tmp_path: Pytest temporary directory fixture
    :type tmp_path: Path
    """
    # Create nested directories
    nested_dir = tmp_path / "models" / "aws"
    nested_dir.mkdir(parents=True)
    test_file = nested_dir / "vpc_model.py"
    test_file.write_text("# VPC model")

    # Test with backslash path (simulating Windows)
    original_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        result = get_path("models\\aws\\vpc_model")
        assert os.path.isabs(result)
        assert "vpc_model" in result
        assert not result.endswith(".py")
    finally:
        os.chdir(original_cwd)


# Tests for get_module_path function
def test_get_module_path_with_valid_package(tmp_path: Path) -> None:
    """
    Test get_module_path correctly resolves valid Python package structure.

    :param tmp_path: Pytest temporary directory fixture
    :type tmp_path: Path
    """
    # Create a proper Python package structure
    package_dir = tmp_path / "models"
    package_dir.mkdir()
    (package_dir / "__init__.py").write_text("# Package init")

    subpackage_dir = package_dir / "aws"
    subpackage_dir.mkdir()
    (subpackage_dir / "__init__.py").write_text("# Subpackage init")

    module_file = subpackage_dir / "vpc_builder"

    base_path, module_name = get_module_path(str(module_file))

    assert base_path == str(tmp_path)
    assert module_name == "models.aws.vpc_builder"


def test_get_module_path_with_missing_init_file(tmp_path: Path) -> None:
    """
    Test get_module_path raises ModuleNotFoundError when __init__.py is missing.

    :param tmp_path: Pytest temporary directory fixture
    :type tmp_path: Path
    """
    # Create directory without __init__.py
    package_dir = tmp_path / "models"
    package_dir.mkdir()
    module_file = package_dir / "test_module"

    with pytest.raises(ModuleNotFoundError, match="No Python package found"):
        get_module_path(str(module_file))


def test_get_module_path_with_empty_path() -> None:
    """
    Test get_module_path raises ValueError for empty file path.
    """
    with pytest.raises(ValueError, match="File path must be a non-empty string"):
        get_module_path("")


def test_get_module_path_with_none_input() -> None:
    """
    Test get_module_path raises ValueError for None input.
    """
    with pytest.raises(ValueError, match="File path must be a non-empty string"):
        get_module_path(None)


def test_get_module_path_with_deeply_nested_package(tmp_path: Path) -> None:
    """
    Test get_module_path handles deeply nested package structures.

    :param tmp_path: Pytest temporary directory fixture
    :type tmp_path: Path
    """
    # Create deeply nested package structure
    nested_path = tmp_path / "models" / "aws" / "vpc" / "components"
    nested_path.mkdir(parents=True)

    # Create __init__.py files at each level
    for path in [
        tmp_path / "models",
        tmp_path / "models" / "aws",
        tmp_path / "models" / "aws" / "vpc",
        nested_path,
    ]:
        (path / "__init__.py").write_text("# Package init")

    module_file = nested_path / "subnet_builder"

    base_path, module_name = get_module_path(str(module_file))

    assert base_path == str(tmp_path)
    assert module_name == "models.aws.vpc.components.subnet_builder"


def test_get_module_path_with_root_package_only(tmp_path: Path) -> None:
    """
    Test get_module_path handles single-level package correctly.

    :param tmp_path: Pytest temporary directory fixture
    :type tmp_path: Path
    """
    # Create simple package structure
    package_dir = tmp_path / "utilities"
    package_dir.mkdir()
    (package_dir / "__init__.py").write_text("# Utilities package")

    module_file = package_dir / "helper_functions"

    base_path, module_name = get_module_path(str(module_file))

    assert base_path == str(tmp_path)
    assert module_name == "utilities.helper_functions"


# Tests for run_module function
def test_run_module_successful_execution(mock_ansible_module: Mock) -> None:
    """
    Test successful module execution with valid model.

    :param mock_ansible_module: Mocked AnsibleModule instance from conftest
    :type mock_ansible_module: Mock
    """
    # Setup mock model
    mock_model_instance = MockModel("successful output")

    with (
        patch("generate_model.AnsibleModule", return_value=mock_ansible_module),
        patch("generate_model.get_path", return_value="/tmp/test_model"),
        patch("generate_model.get_module_path", return_value=("/tmp", "test_model")),
        patch("generate_model.import_module") as mock_import,
        patch("generate_model.stringcase.pascalcase", return_value="TestModel"),
    ):
        # Setup mock module with mock model class
        mock_imported_module = Mock()
        mock_imported_module.TestModel = Mock(return_value=mock_model_instance)
        mock_import.return_value = mock_imported_module

        run_module()

        # Verify model was executed
        assert mock_model_instance.generate_called
        assert mock_model_instance.generate_kwargs["params"] == {"key": "value"}
        assert mock_model_instance.generate_kwargs["description"] == "Test description"

        # Verify successful exit
        mock_ansible_module.exit_json.assert_called_once()
        exit_args = mock_ansible_module.exit_json.call_args[1]
        assert exit_args["output"] == "successful output"


def test_run_module_file_not_found_error(mock_ansible_module: Mock) -> None:
    """
    Test module execution handles FileNotFoundError gracefully.

    :param mock_ansible_module: Mocked AnsibleModule instance from conftest
    :type mock_ansible_module: Mock
    """
    with (
        patch("generate_model.AnsibleModule", return_value=mock_ansible_module),
        patch(
            "generate_model.get_path", side_effect=FileNotFoundError("File not found")
        ),
    ):
        run_module()

        mock_ansible_module.fail_json.assert_called_once()
        fail_args = mock_ansible_module.fail_json.call_args[1]
        assert "Model path validation failed" in fail_args["msg"]


def test_run_module_empty_model_parameter(mock_ansible_module: Mock) -> None:
    """
    Test module execution handles empty model parameter.

    :param mock_ansible_module: Mocked AnsibleModule instance from conftest
    :type mock_ansible_module: Mock
    """
    with (
        patch("generate_model.AnsibleModule", return_value=mock_ansible_module),
        patch(
            "generate_model.get_path",
            side_effect=ValueError("Model parameter cannot be empty"),
        ),
    ):
        run_module()

        mock_ansible_module.fail_json.assert_called_once()
        fail_args = mock_ansible_module.fail_json.call_args[1]
        assert "Model path validation failed" in fail_args["msg"]


def test_run_module_import_error(mock_ansible_module: Mock) -> None:
    """
    Test module execution handles ImportError gracefully.

    :param mock_ansible_module: Mocked AnsibleModule instance from conftest
    :type mock_ansible_module: Mock
    """
    with (
        patch("generate_model.AnsibleModule", return_value=mock_ansible_module),
        patch("generate_model.get_path", return_value="/tmp/test_model"),
        patch("generate_model.get_module_path", return_value=("/tmp", "test_model")),
        patch(
            "generate_model.import_module",
            side_effect=ImportError("Cannot import module"),
        ),
    ):
        run_module()

        mock_ansible_module.fail_json.assert_called_once()
        fail_args = mock_ansible_module.fail_json.call_args[1]
        assert "Cannot import module" in fail_args["msg"]


def test_run_module_missing_class(mock_ansible_module: Mock) -> None:
    """
    Test module execution handles missing model class.

    :param mock_ansible_module: Mocked AnsibleModule instance from conftest
    :type mock_ansible_module: Mock
    """
    with (
        patch("generate_model.AnsibleModule", return_value=mock_ansible_module),
        patch("generate_model.get_path", return_value="/tmp/test_model"),
        patch("generate_model.get_module_path", return_value=("/tmp", "test_model")),
        patch("generate_model.import_module") as mock_import,
        patch("generate_model.stringcase.pascalcase", return_value="TestModel"),
    ):
        # Setup mock module without the expected class
        mock_imported_module = Mock(spec=[])  # Empty spec means no attributes
        del mock_imported_module.TestModel  # Ensure attribute doesn't exist
        mock_import.return_value = mock_imported_module

        run_module()

        mock_ansible_module.fail_json.assert_called_once()
        fail_args = mock_ansible_module.fail_json.call_args[1]
        assert "Class 'TestModel' not found" in fail_args["msg"]


def test_run_module_class_instantiation_error(mock_ansible_module: Mock) -> None:
    """
    Test module execution handles class instantiation errors.

    :param mock_ansible_module: Mocked AnsibleModule instance from conftest
    :type mock_ansible_module: Mock
    """
    with (
        patch("generate_model.AnsibleModule", return_value=mock_ansible_module),
        patch("generate_model.get_path", return_value="/tmp/test_model"),
        patch("generate_model.get_module_path", return_value=("/tmp", "test_model")),
        patch("generate_model.import_module") as mock_import,
        patch("generate_model.stringcase.pascalcase", return_value="TestModel"),
    ):
        # Setup mock module with class that raises error on instantiation
        mock_class = Mock(side_effect=TypeError("Missing required argument"))
        mock_imported_module = Mock()
        mock_imported_module.TestModel = mock_class
        mock_import.return_value = mock_imported_module

        run_module()

        mock_ansible_module.fail_json.assert_called_once()
        fail_args = mock_ansible_module.fail_json.call_args[1]
        assert "Cannot instantiate class 'TestModel'" in fail_args["msg"]


def test_run_module_missing_generate_method(mock_ansible_module: Mock) -> None:
    """
    Test module execution handles missing generate method.

    :param mock_ansible_module: Mocked AnsibleModule instance from conftest
    :type mock_ansible_module: Mock
    """
    with (
        patch("generate_model.AnsibleModule", return_value=mock_ansible_module),
        patch("generate_model.get_path", return_value="/tmp/test_model"),
        patch("generate_model.get_module_path", return_value=("/tmp", "test_model")),
        patch("generate_model.import_module") as mock_import,
        patch("generate_model.stringcase.pascalcase", return_value="TestModel"),
    ):
        # Setup mock model instance without generate method
        mock_instance = Mock(spec=[])  # No generate method
        mock_class = Mock(return_value=mock_instance)
        mock_imported_module = Mock()
        mock_imported_module.TestModel = mock_class
        mock_import.return_value = mock_imported_module

        run_module()

        mock_ansible_module.fail_json.assert_called_once()
        fail_args = mock_ansible_module.fail_json.call_args[1]
        assert "must implement a 'generate' method" in fail_args["msg"]


def test_run_module_generate_method_exception(mock_ansible_module: Mock) -> None:
    """
    Test module execution handles exceptions from generate method.

    :param mock_ansible_module: Mocked AnsibleModule instance from conftest
    :type mock_ansible_module: Mock
    """
    with (
        patch("generate_model.AnsibleModule", return_value=mock_ansible_module),
        patch("generate_model.get_path", return_value="/tmp/test_model"),
        patch("generate_model.get_module_path", return_value=("/tmp", "test_model")),
        patch("generate_model.import_module") as mock_import,
        patch("generate_model.stringcase.pascalcase", return_value="TestModel"),
    ):
        # Setup mock model that raises exception in generate method
        mock_instance = Mock()
        mock_instance.generate.side_effect = RuntimeError("Model execution failed")
        mock_class = Mock(return_value=mock_instance)
        mock_imported_module = Mock()
        mock_imported_module.TestModel = mock_class
        mock_import.return_value = mock_imported_module

        run_module()

        mock_ansible_module.fail_json.assert_called_once()
        fail_args = mock_ansible_module.fail_json.call_args[1]
        assert "Error executing generate() method" in fail_args["msg"]
        assert "traceback" in fail_args


def test_run_module_dict_response(mock_ansible_module: Mock) -> None:
    """
    Test module execution handles dictionary response from generate method.

    :param mock_ansible_module: Mocked AnsibleModule instance from conftest
    :type mock_ansible_module: Mock
    """
    # Setup mock model that returns dict
    mock_model_instance = MockModel(
        {"output": "dict output", "changed": True, "custom_key": "custom_value"}
    )

    with (
        patch("generate_model.AnsibleModule", return_value=mock_ansible_module),
        patch("generate_model.get_path", return_value="/tmp/test_model"),
        patch("generate_model.get_module_path", return_value=("/tmp", "test_model")),
        patch("generate_model.import_module") as mock_import,
        patch("generate_model.stringcase.pascalcase", return_value="TestModel"),
    ):
        mock_imported_module = Mock()
        mock_imported_module.TestModel = Mock(return_value=mock_model_instance)
        mock_import.return_value = mock_imported_module

        run_module()

        mock_ansible_module.exit_json.assert_called_once()
        exit_args = mock_ansible_module.exit_json.call_args[1]
        assert exit_args["output"] == "dict output"
        assert exit_args["changed"] is True
        assert exit_args["custom_key"] == "custom_value"


def test_run_module_none_response(mock_ansible_module: Mock) -> None:
    """
    Test module execution handles None response from generate method.

    :param mock_ansible_module: Mocked AnsibleModule instance from conftest
    :type mock_ansible_module: Mock
    """
    # Setup mock model that returns None
    mock_model_instance = MockModel(None)

    with (
        patch("generate_model.AnsibleModule", return_value=mock_ansible_module),
        patch("generate_model.get_path", return_value="/tmp/test_model"),
        patch("generate_model.get_module_path", return_value=("/tmp", "test_model")),
        patch("generate_model.import_module") as mock_import,
        patch("generate_model.stringcase.pascalcase", return_value="TestModel"),
    ):
        mock_imported_module = Mock()
        mock_imported_module.TestModel = Mock(return_value=mock_model_instance)
        mock_import.return_value = mock_imported_module

        run_module()

        mock_ansible_module.exit_json.assert_called_once()
        exit_args = mock_ansible_module.exit_json.call_args[1]
        assert exit_args["output"] == ""


# Tests for main function
@patch("generate_model.run_module")
def test_main_calls_run_module(mock_run_module: Mock) -> None:
    """
    Test main function properly delegates to run_module.

    :param mock_run_module: Mocked run_module function
    :type mock_run_module: Mock
    """
    main()
    mock_run_module.assert_called_once()


# Tests for stringcase integration
def test_snake_case_to_pascal_case_conversion() -> None:
    """
    Test stringcase properly converts snake_case to PascalCase.
    """
    test_cases = [
        ("vpc_builder", "VpcBuilder"),
        ("simple_model", "SimpleModel"),
        ("aws_ec2_instance", "AwsEc2Instance"),
        ("test", "Test"),
        ("multi_word_long_name", "MultiWordLongName"),
    ]

    for snake_case, expected_pascal in test_cases:
        result = stringcase.pascalcase(snake_case)
        assert result == expected_pascal, f"Expected {expected_pascal}, got {result}"
