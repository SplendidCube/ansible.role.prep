# Helpers Module

The helpers module provides abstract base classes and utilities for building AWS resource models and CloudFormation templates.

## Module Overview

```{eval-rst}
.. automodule:: helpers
   :members:
   :undoc-members:
   :show-inheritance:
```

## AWS Resource Model

The `AwsResourceModel` class provides a standardized interface for AWS resource operations within Ansible modules.

```{eval-rst}
.. automodule:: helpers.aws_resource_model
   :members:
   :undoc-members:
   :show-inheritance:
```

### AWS Resource Model Features

- **YAML Response Generation**: Standardized output format for Ansible integration
- **Parameter Processing**: Flexible parameter handling and validation
- **Error Management**: Comprehensive error handling with Ansible integration
- **Abstract Interface**: Enforces implementation of core functionality

### AWS Resource Model Example

```python
from helpers.aws_resource_model import AwsResourceModel

class MyResourceModel(AwsResourceModel):
    def run(self, params, response):
        # Implement your AWS resource logic here
        response["ResourceId"] = "my-resource-123"
        response["Status"] = "Created"
        return {"additional": "data"}
```

## CloudFormation Builder

The `CfnBuilder` class provides a framework for building CloudFormation templates using Troposphere.

```{eval-rst}
.. automodule:: helpers.cfn_builder
   :members:
   :undoc-members:
   :show-inheritance:
```

### CloudFormation Builder Features

- **Template Generation**: Automated CloudFormation template creation
- **Parameter Filtering**: Smart parameter processing and validation
- **Extensible Architecture**: Abstract methods for custom implementations
- **Troposphere Integration**: Built on the robust Troposphere library

### CloudFormation Builder Example

```python
from helpers.cfn_builder import CfnBuilder
from troposphere import s3

class MyTemplateBuilder(CfnBuilder):
    def _build(self, cfn_template, params):
        # Add your CloudFormation resources
        bucket = s3.Bucket("MyBucket")
        cfn_template.add_resource(bucket)
        return cfn_template
```
