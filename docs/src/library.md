# Library Module

The library module contains Ansible modules that provide dynamic model execution capabilities.

## Module Overview

```{eval-rst}
.. automodule:: library
   :members:
   :undoc-members:
   :show-inheritance:
```

## Model Generate Module

The `generate_model` module enables dynamic execution of Python models from within Ansible playbooks.

```{eval-rst}
.. automodule:: library.generate_model
   :members:
   :undoc-members:
   :show-inheritance:
```

### Module Features

- **Dynamic Loading**: Load Python models dynamically based on file/class naming conventions
- **Ansible Integration**: Full integration with Ansible module framework
- **Error Handling**: Comprehensive error handling with detailed failure messages
- **Model Discovery**: Automatic model path resolution and class instantiation

### Module Parameters

The `generate_model` module accepts the following parameters:

- **`file`** (required): Path to the Python file containing the model class
- **`class_name`** (optional): Name of the class to instantiate (defaults to PascalCase of filename)
- **`description`** (optional): Description to pass to the model's generate method
- **Additional parameters**: Any additional parameters are passed to the model's generate method

### Usage in Ansible Playbooks

```yaml
- name: Execute custom CloudFormation model
  generate_model:
    file: /path/to/models/my_infrastructure.py
    class_name: MyInfrastructure
    description: "Deploy web application infrastructure"
    environment: production
    region: us-west-2
```

### Model Development

Models must implement a `generate` method with the following signature:

```python
def generate(self, params: dict, description: str, ansible: AnsibleModule) -> str:
    """
    Generate output based on the provided parameters.

    :param params: Dictionary of parameters from Ansible
    :param description: Description string from Ansible
    :param ansible: AnsibleModule instance for integration
    :returns: Generated output (typically YAML or JSON)
    """
    # Your implementation here
    pass
```

### Integration with Helper Classes

The module works seamlessly with the helper classes:

```python
from helpers.aws_resource_model import AwsResourceModel
from helpers.cfn_builder import CfnBuilder

class InfrastructureModel(AwsResourceModel, CfnBuilder):
    def generate(self, params, description, ansible):
        # Use both AWS resource and CloudFormation capabilities
        return self.generate_yaml(params, ansible, description)

    def run(self, params, response):
        # AWS resource logic
        pass

    def _build(self, cfn_template, params):
        # CloudFormation template building
        return cfn_template
```
