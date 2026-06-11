"""
cli/user_commands.py
Argparse subcommand handlers for user management.
"""
import logging

from models.user import User
from utils.display import display_users, print_success, print_error, print_info
from utils.validators import validate_email, validate_role

logger = logging.getLogger(__name__)


def cmd_add_user(args, users: list) -> bool:
    """
    Handle: add-user --name <name> [--email <email>] [--role <role>]
    Returns True if state was modified.
    """
    # Validate email
    if args.email and not validate_email(args.email):
        print_error(f"Invalid email address: '{args.email}'")
        return False

    # Validate role
    if args.role and not validate_role(args.role):
        print_error(f"Invalid role '{args.role}'. Choose from: admin, member")
        return False

    # Prevent duplicate names
    for u in users:
        if u.name.lower() == args.name.lower():
            print_error(f"User '{args.name}' already exists (ID {u.id}).")
            return False

    user = User(
        name=args.name,
        email=args.email or "",
        role=args.role or "member",
    )
    users.append(user)
    print_success(f"User '{user.name}' created (ID {user.id}).")
    logger.info("Created user: %r", user)
    return True


def cmd_list_users(args, users: list) -> bool:
    """Handle: list-users"""
    display_users(users)
    return False


def cmd_update_user(args, users: list) -> bool:
    """
    Handle: update-user --name <name> [--new-name <n>] [--email <e>] [--role <r>]
    Returns True if state was modified.
    """
    user = _find_user(args.name, users)
    if not user:
        return False

    changed = False

    if args.new_name:
        # Check duplicate
        for u in users:
            if u.id != user.id and u.name.lower() == args.new_name.lower():
                print_error(f"Another user named '{args.new_name}' already exists.")
                return False
        user.name = args.new_name
        changed = True

    if args.email:
        if not validate_email(args.email):
            print_error(f"Invalid email: '{args.email}'")
            return False
        user.email = args.email
        changed = True

    if args.role:
        if not validate_role(args.role):
            print_error(f"Invalid role '{args.role}'. Choose from: admin, member")
            return False
        user.role = args.role
        changed = True

    if changed:
        print_success(f"User '{user.name}' updated.")
        logger.info("Updated user: %r", user)
    else:
        print_info("Nothing to update — provide at least one of: --new-name, --email, --role")

    return changed


def cmd_delete_user(args, users: list) -> bool:
    """Handle: delete-user --name <name>"""
    user = _find_user(args.name, users)
    if not user:
        return False

    users.remove(user)
    print_success(f"User '{user.name}' deleted.")
    logger.info("Deleted user: %r", user)
    return True


# ── Internal helpers ───────────────────────────────────────────────────────────

def _find_user(name: str, users: list) -> User | None:
    """Find a user by name; print error if not found."""
    for u in users:
        if u.name.lower() == name.lower():
            return u
    print_error(f"User '{name}' not found.")
    return None
