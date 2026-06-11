"""
cli/project_commands.py
Argparse subcommand handlers for project management.
"""
import logging

from models.project import Project
from utils.display import display_projects, print_success, print_error, print_info
from utils.validators import validate_date

logger = logging.getLogger(__name__)


def cmd_add_project(args, users: list) -> bool:
    """
    Handle: add-project --user <name> --title <title>
            [--description <desc>] [--due-date YYYY-MM-DD]
    """
    user = _find_user(args.user, users)
    if not user:
        return False

    if args.due_date and not validate_date(args.due_date):
        print_error("due_date must be in YYYY-MM-DD format.")
        return False

    # Prevent duplicate project titles for this user
    if user.get_project_by_title(args.title):
        print_error(
            f"User '{user.name}' already has a project titled '{args.title}'."
        )
        return False

    project = Project(
        title=args.title,
        description=args.description or "",
        due_date=args.due_date or "",
    )
    user.add_project(project)
    print_success(
        f"Project '{project.title}' added to user '{user.name}' (Project ID {project.id})."
    )
    logger.info("Created project: %r for user %r", project, user)
    return True


def cmd_list_projects(args, users: list) -> bool:
    """Handle: list-projects [--user <name>]"""
    if args.user:
        user = _find_user(args.user, users)
        if not user:
            return False
        display_projects(user.projects, owner_name=user.name)
    else:
        # Aggregate all projects across all users
        all_projects = []
        for u in users:
            all_projects.extend(u.projects)
        display_projects(all_projects)
    return False


def cmd_update_project(args, users: list) -> bool:
    """
    Handle: update-project --user <name> --title <title>
            [--new-title <t>] [--description <d>] [--due-date <d>]
    """
    user = _find_user(args.user, users)
    if not user:
        return False

    project = user.get_project_by_title(args.title)
    if not project:
        print_error(f"Project '{args.title}' not found for user '{user.name}'.")
        return False

    changed = False

    if args.new_title:
        if user.get_project_by_title(args.new_title):
            print_error(
                f"A project titled '{args.new_title}' already exists for '{user.name}'."
            )
            return False
        project.title = args.new_title
        changed = True

    if args.description is not None:
        project.description = args.description
        changed = True

    if args.due_date is not None:
        if not validate_date(args.due_date):
            print_error("due_date must be in YYYY-MM-DD format.")
            return False
        project.due_date = args.due_date
        changed = True

    if changed:
        print_success(f"Project updated successfully.")
        logger.info("Updated project: %r", project)
    else:
        print_info(
            "Nothing to update — provide at least one of: --new-title, --description, --due-date"
        )

    return changed


def cmd_delete_project(args, users: list) -> bool:
    """Handle: delete-project --user <name> --title <title>"""
    user = _find_user(args.user, users)
    if not user:
        return False

    project = user.get_project_by_title(args.title)
    if not project:
        print_error(f"Project '{args.title}' not found for user '{user.name}'.")
        return False

    user.remove_project(project.id)
    print_success(f"Project '{project.title}' deleted from '{user.name}'.")
    logger.info("Deleted project: %r", project)
    return True


# ── Internal helpers ───────────────────────────────────────────────────────────

def _find_user(name: str, users: list):
    """Find a user by name; print error if not found."""
    for u in users:
        if u.name.lower() == name.lower():
            return u
    print_error(f"User '{name}' not found.")
    return None
