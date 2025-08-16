"""
Shared pytest fixtures for generate_model tests.

This module contains common fixtures used across multiple test modules
to ensure consistent test data and reduce duplication.

Fixture files are stored in the tests/fixtures/ directory as proper Python
files that can be easily edited and maintained. This approach provides:
- Human-readable and editable test data
- Syntax highlighting and IDE support for fixture code
- Version control friendly diffs for changes
- Proper Python formatting and linting
"""

import os
import sys
from pathlib import Path
from typing import Any
from unittest.mock import Mock

import pytest

# Add the library directory to the path for module imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../library"))


@pytest.fixture
def temp_python_package(tmp_path: Path) -> Path:
    """
    Create a temporary Python package structure for integration tests.

    :param tmp_path: Pytest temporary directory fixture
    :type tmp_path: Path
    :returns: Path to the created package directory
    :rtype: Path
    """
    # Get the path to the fixtures directory
    fixtures_dir = Path(__file__).parent.parent / "fixtures"

    # Create the test package
    package_dir = tmp_path / "test_models"
    package_dir.mkdir()

    # Read and write the package __init__.py
    init_content = (fixtures_dir / "package_init.py").read_text()
    (package_dir / "__init__.py").write_text(init_content)

    # Read and write the simple test model
    model_content = (fixtures_dir / "simple_test.py").read_text()
    (package_dir / "simple_test.py").write_text(model_content)

    return package_dir


@pytest.fixture
def failing_package_init() -> str:
    """
    Return test code for a package __init__.py that fails on import.

    :returns: Python code string that raises an ImportError
    :rtype: str
    """
    fixture_path = Path(__file__).parent.parent / "fixtures" / "failing_package_init.py"
    return fixture_path.read_text().strip()


# Helper class fixtures for testing
@pytest.fixture
def aws_model_test() -> str:
    """
    Return test AWS resource model implementation.

    :returns: Python code string for test AWS model
    :rtype: str
    """
    fixture_path = Path(__file__).parent.parent / "fixtures" / "aws_model_test.py"
    return fixture_path.read_text().strip()


@pytest.fixture
def aws_model_no_return() -> str:
    """
    Return test AWS resource model that returns None.

    :returns: Python code string for test AWS model
    :rtype: str
    """
    fixture_path = Path(__file__).parent.parent / "fixtures" / "aws_model_no_return.py"
    return fixture_path.read_text().strip()


@pytest.fixture
def cfn_builder_test() -> str:
    """
    Return test CloudFormation builder implementation.

    :returns: Python code string for test CFN builder
    :rtype: str
    """
    fixture_path = Path(__file__).parent.parent / "fixtures" / "cfn_builder_test.py"
    return fixture_path.read_text().strip()


@pytest.fixture
def cfn_builder_new_template() -> str:
    """
    Return test CloudFormation builder that returns new template.

    :returns: Python code string for test CFN builder
    :rtype: str
    """
    fixture_path = (
        Path(__file__).parent.parent / "fixtures" / "cfn_builder_new_template.py"
    )
    return fixture_path.read_text().strip()


@pytest.fixture
def cfn_builder_custom_filter() -> str:
    """
    Return test CloudFormation builder with custom parameter filtering.

    :returns: Python code string for test CFN builder
    :rtype: str
    """
    fixture_path = (
        Path(__file__).parent.parent / "fixtures" / "cfn_builder_custom_filter.py"
    )
    return fixture_path.read_text().strip()


@pytest.fixture
def cfn_builder_custom_init() -> str:
    """
    Return test CloudFormation builder with custom initialization.

    :returns: Python code string for test CFN builder
    :rtype: str
    """
    fixture_path = (
        Path(__file__).parent.parent / "fixtures" / "cfn_builder_custom_init.py"
    )
    return fixture_path.read_text().strip()


@pytest.fixture
def cfn_builder_error() -> str:
    """
    Return test CloudFormation builder that raises an exception.

    :returns: Python code string for test CFN builder
    :rtype: str
    """
    fixture_path = Path(__file__).parent.parent / "fixtures" / "cfn_builder_error.py"
    return fixture_path.read_text().strip()


class MockModel:
    """
    Mock model class for testing module execution.
    """

    def __init__(self, return_value: Any = "test output"):
        """
        Initialize mock model.

        :param return_value: Value to return from generate method
        :type return_value: Any
        """
        self.return_value = return_value
        self.generate_called = False
        self.generate_args = None
        self.generate_kwargs = None

    def generate(self, params: dict[str, Any], description: str, ansible: Any) -> Any:
        """
        Mock generate method that records call parameters.

        :param params: Parameters dictionary
        :type params: Dict[str, Any]
        :param description: Description string
        :type description: str
        :param ansible: Ansible module instance
        :type ansible: Any
        :returns: Configured return value
        :rtype: Any
        """
        self.generate_called = True
        self.generate_args = (params, description, ansible)
        self.generate_kwargs = {
            "params": params,
            "description": description,
            "ansible": ansible,
        }
        return self.return_value


@pytest.fixture
def mock_model() -> MockModel:
    """
    Create a standard MockModel instance for testing.

    :returns: Initialized MockModel instance
    :rtype: MockModel
    """
    return MockModel("test output")


@pytest.fixture
def mock_ansible_module() -> Mock:
    """
    Create a mock AnsibleModule instance for testing.

    :returns: Mock AnsibleModule with standard configuration
    :rtype: Mock
    """
    mock_module = Mock()
    mock_module.params = {
        "model": "test_model",
        "parameters": {"key": "value"},
        "description": "Test description",
    }
    return mock_module
