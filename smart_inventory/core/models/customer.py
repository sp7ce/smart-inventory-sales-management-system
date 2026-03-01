"""Customer model — represents a registered customer.

Includes email validation logic.
"""

from __future__ import annotations

import re

from core.exceptions import InvalidEmailException


class Customer:
    """A customer in the Smart Inventory system.

    Attributes:
        id: Unique identifier.
        name: Full name.
        email: Email address (validated on creation).
    """

    _EMAIL_REGEX = re.compile(
        r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    )

    def __init__(self, id: int, name: str, email: str) -> None:
        self.id: int = id
        self.name: str = name
        self.email: str = email
        self.validate_email()

    def validate_email(self) -> bool:
        """Validate the customer's email address.

        Returns:
            True if the email is valid.

        Raises:
            InvalidEmailException: If the email does not match the pattern.
        """
        if not self._EMAIL_REGEX.match(self.email):
            raise InvalidEmailException(email=self.email)
        return True

    def __repr__(self) -> str:
        return f"Customer(id={self.id}, name='{self.name}', email='{self.email}')"

    def __str__(self) -> str:
        return f"{self.name} <{self.email}>"
