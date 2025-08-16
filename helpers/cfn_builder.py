"""
CloudFormation template builder using Troposphere.
"""

import traceback
from abc import ABC, abstractmethod
from typing import Any

from ansible.module_utils.basic import AnsibleModule
from troposphere import Template


class CfnBuilder(ABC):
    """
    Abstract CloudFormation builder for creating AWS templates with Troposphere.

    This class provides a comprehensive framework for building AWS CloudFormation
    templates using Troposphere's Python DSL. It includes built-in error handling,
    parameter filtering, and template generation capabilities.

    The builder follows a structured workflow:

    1. Parameter filtering and validation
    2. Template initialization with common settings
    3. Resource construction via the abstract _build method
    4. YAML output generation

    :cvar counter: Class-level counter for generating unique resource names
    :vartype counter: int
    :ivar ansible: AnsibleModule instance for logging and error handling
    :vartype ansible: AnsibleModule
    """

    counter: int = 0
    ansible: AnsibleModule

    def generate(
        self, params: dict[str, Any], description: str, ansible: AnsibleModule
    ) -> str:
        """
        Generate a CloudFormation template and return it as YAML.

        This method orchestrates the complete template generation workflow,
        including parameter processing, template building, and error handling.

        :param params: Dictionary of parameters for template generation
        :type params: Dict[str, Any]
        :param description: Human-readable description for the CloudFormation template
        :type description: str
        :param ansible: AnsibleModule instance for error handling and logging
        :type ansible: AnsibleModule
        :returns: YAML-formatted CloudFormation template as a string
        :rtype: str
        :raises AnsibleFailJson: If any error occurs during template generation
        """
        self.ansible = ansible
        cfn_template: Template | None = None

        try:
            # Filter and validate input parameters
            filtered_params = self._filter_params(params)

            # Initialize the base template with common settings
            cfn_template = self._init(filtered_params, description)

            # Build the template using the abstract method
            built_template = self._build(cfn_template, filtered_params)

            # Allow models to return a new template object if needed
            if built_template:
                cfn_template = built_template

        except Exception as e:
            self.ansible.fail_json(
                msg=f"CloudFormation template generation failed: {e}",
                traceback=traceback.format_exc(),
            )
            # This line should never be reached due to fail_json, but helps with type checking
            return ""  # pragma: no cover

        return cfn_template.to_yaml()

    @abstractmethod
    def _build(self, cfn_template: Template, params: dict[str, Any]) -> Template | None:
        """
        Build the core CloudFormation template resources.

        This method must be implemented by all subclasses to define the specific
        AWS resources, parameters, outputs, and conditions for their templates.

        :param cfn_template: Initialized Troposphere Template object
        :type cfn_template: Template
        :param params: Filtered parameters dictionary for template construction
        :type params: Dict[str, Any]
        :returns: Optional Template object if a new template should replace the original. Return None to continue using the passed template object
        :rtype: Template or None
        """
        ...

    def _init(
        self,
        _params: dict[str, Any],  # Available for subclass overrides
        description: str | None,
    ) -> Template:
        """
        Initialize the base CloudFormation template with common settings.

        This method can be overridden by subclasses to customize template
        initialization, add common parameters, or set template metadata.

        :param _params: Filtered parameters dictionary (available for custom logic)
        :type _params: Dict[str, Any]
        :param description: Optional template description to include
        :type description: str or None
        :returns: Initialized Troposphere Template object with version and description
        :rtype: Template
        """
        cfn_template = Template()
        cfn_template.set_version()

        if description:
            cfn_template.set_description(description)

        return cfn_template

    def _filter_params(self, params: dict[str, Any]) -> dict[str, Any]:
        """
        Filter and validate parameters for template generation.

        Override this method in subclasses to implement parameter validation,
        transformation, or filtering logic specific to each template type.

        :param params: Raw parameters dictionary from Ansible
        :type params: Dict[str, Any]
        :returns: Filtered and validated parameters dictionary
        :rtype: Dict[str, Any]
        """
        return params

    @classmethod
    def increment(cls, start: int = 1) -> int:
        """
        Increment and return a class-level counter for unique naming.

        This counter is shared across all instances of the same class and
        is commonly used for generating unique resource names when creating
        multiple resources of the same type.

        :param start: Starting value for the counter
        :type start: int
        :returns: The current counter value after incrementing
        :rtype: int

        Example::

            >>> builder = MyCloudFormationBuilder()
            >>> name = f"MyResource{builder.increment()}"  # "MyResource1"
            >>> name = f"MyResource{builder.increment()}"  # "MyResource2"
        """
        cls.counter = cls.counter + 1 if cls.counter else start
        return cls.counter
