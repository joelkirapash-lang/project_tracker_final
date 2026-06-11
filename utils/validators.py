"""
utils/validators.py
Input validation helpers used across CLI commands.
"""
import re
from datetime import datetime


def validate_email(email: str) -> bool:
    """
    Return True if the email address looks valid.
    Uses a basic regex pattern; not RFC-5321 exhaustive.
    """
    if not email:
        return True  # email is optional
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return bool(re.match(pattern, email))


def validate_date(date_str: str) -> bool:
    """
    Return True if date_str matches YYYY-MM-DD format.
    Returns True for empty string (date is optional).
    """
    if not date_str:
        return True
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_status(status: str) -> bool:
    """Return True if the status is one of the accepted values."""
    return status in ("todo", "in_progress", "done")


def validate_role(role: str) -> bool:
    """Return True if the role is one of the accepted values."""
    return role in ("admin", "member")
