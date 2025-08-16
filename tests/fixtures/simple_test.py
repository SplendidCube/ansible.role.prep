"""Simple test model for integration testing."""


class SimpleTest:
    """Test model class."""

    def generate(self, params, description, ansible):
        """Generate test output."""
        return f"Generated with params: {params}, description: {description}"
