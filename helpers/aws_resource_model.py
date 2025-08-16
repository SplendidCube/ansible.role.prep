"""
AWS resource model base class for Ansible module integration.
"""

from abc import ABC, abstractmethod

import yaml
from ansible.module_utils.basic import AnsibleModule


class AwsResourceModel(ABC):
    """
    Abstract base class for AWS resource models that can be executed when
    used with the generate_model Ansible module. It handles the standard
    workflow of parameter processing, model execution, and response formatting.

    :ivar ansible: The AnsibleModule instance for logging and error handling
    :vartype ansible: AnsibleModule
    """

    def generate(
        self, params: dict, ansible: AnsibleModule, description: str | None = None
    ) -> str:
        """
        Main entry point for the generate_model Ansible module.

        Processes parameters, executes the model logic, and returns a formatted
        YAML response suitable for Ansible consumption.

        :param params: Dictionary of parameters to pass to the model
        :type params: dict
        :param ansible: AnsibleModule instance for logging and error handling
        :type ansible: AnsibleModule
        :param description: Optional description to include in the response
        :type description: str or None
        :returns: YAML-formatted string containing the model response
        :rtype: str
        """
        response: dict = {}
        self.ansible = ansible

        if description:
            response["Description"] = description

        response_update = self.run(params=params, response=response)

        # Allow models to return additional response data
        if response_update:
            response.update(response_update)

        return yaml.dump(response, default_flow_style=False)

    @abstractmethod
    def run(self, params: dict, response: dict) -> dict | None:
        """
        Execute the core functionality of the AWS resource model.

        This method must be implemented by all subclasses to define the
        specific behavior for each AWS resource type.

        :param params: Dictionary of parameters passed to the model
        :type params: dict
        :param response: Mutable response dictionary that can be modified directly
        :type response: dict
        :returns: Optional dictionary of additional response data to merge with the main response. Can return None if response dict is modified directly
        :rtype: dict or None
        """
        ...
