"""Model that always fails for testing error handling."""


class AlwaysFails:
    """Model that raises exceptions."""

    def generate(self, params, description, ansible):
        """Always raise an exception."""
        raise RuntimeError("This model always fails")
