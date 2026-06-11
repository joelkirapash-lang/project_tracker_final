"""
models/person.py
Base class for all people in the system.
Demonstrates inheritance — User will extend Person.
"""


class Person:
    """Base class representing a person with a name and email."""

    def __init__(self, name: str, email: str):
        """Initialize a Person with a name and email."""
        self._name = name
        self._email = email

    @property
    def name(self) -> str:
        """Get the person's name."""
        return self._name

    @name.setter
    def name(self, value: str):
        """Set the person's name with validation."""
        if not value or not value.strip():
            raise ValueError("Name cannot be empty.")
        self._name = value.strip()

    @property
    def email(self) -> str:
        """Get the person's email."""
        return self._email

    @email.setter
    def email(self, value: str):
        """Set the person's email with basic validation."""
        if value and "@" not in value:
            raise ValueError("Invalid email address.")
        self._email = value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self._name!r}, email={self._email!r})"
