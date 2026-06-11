"""
cli/task_commands.py
Argparse subcommand handlers for task management.
"""
import logging

from models.task import Task
from utils.display import display_tasks, print_success, print_error, print_info
from utils.validators import validate_status

logger = logging.getLogger(__name__)


def cmd_add_task(args, users: list) -> bool:
    """
    Handle: add-task --project <title> --title <task_title>
            [--assigned-to <name>] [--status <status>]
    Searches across all users' projects.
    """
    project = _find_project(args.project, users)
    if not project:
        return False

    if args.status and not validate_status(args.status):
        print_error(
            f"Invalid status '{args.status}'. Choose from: todo, in_progress, done"
        )
        return False

    # Prevent duplicate task titles within the same project
    if project.get_task_by_title(args.title):
        print_error(
            f"Task '{args.title}' already exists in project '{project.title}'."
        )
        return False

    task = Task(
        title=args.title,
        status=args.status or "todo",
        assigned_to=args.assigned_to or "",
    )
    project.add_task(task)
    print_success(
        f"Task '{task.title}' added to project '{project.title}' (Task ID {task.id})."
    )
    logger.info("Created task: %r in project %r", task, project)
    return True


def cmd_list_tasks(args, users: list) -> bool:
    """Handle: list-tasks --project <title>"""
    project = _find_project(args.project, users)
    if not project:
        return False
    display_tasks(project.tasks, project_title=project.title)
    return False


def cmd_complete_task(args, users: list) -> bool:
    """Handle: complete-task --project <title> --title <task_title>"""
    project = _find_project(args.project, users)
    if not project:
        return False

    task = project.get_task_by_title(args.title)
    if not task:
        print_error(f"Task '{args.title}' not found in project '{project.title}'.")
        return False

    if task.status == "done":
        print_info(f"Task '{task.title}' is already marked as done.")
        return False

    task.complete()
    print_success(f"Task '{task.title}' marked as done ✔")
    logger.info("Completed task: %r", task)
    return True


def cmd_update_task(args, users: list) -> bool:
    """
    Handle: update-task --project <title> --title <task_title>
            [--new-title <t>] [--status <s>] [--assigned-to <a>]
    """
    project = _find_project(args.project, users)
    if not project:
        return False

    task = project.get_task_by_title(args.title)
    if not task:
        print_error(f"Task '{args.title}' not found in project '{project.title}'.")
        return False

    changed = False

    if args.new_title:
        if project.get_task_by_title(args.new_title):
            print_error(
                f"A task titled '{args.new_title}' already exists in this project."
            )
            return False
        task.title = args.new_title
        changed = True

    if args.status:
        if not validate_status(args.status):
            print_error(
                f"Invalid status '{args.status}'. Choose from: todo, in_progress, done"
            )
            return False
        task.status = args.status
        changed = True

    if args.assigned_to is not None:
        task.assigned_to = args.assigned_to
        changed = True

    if changed:
        print_success(f"Task updated successfully.")
        logger.info("Updated task: %r", task)
    else:
        print_info(
            "Nothing to update — provide at least one of: --new-title, --status, --assigned-to"
        )

    return changed


def cmd_delete_task(args, users: list) -> bool:
    """Handle: delete-task --project <title> --title <task_title>"""
    project = _find_project(args.project, users)
    if not project:
        return False

    task = project.get_task_by_title(args.title)
    if not task:
        print_error(f"Task '{args.title}' not found in project '{project.title}'.")
        return False

    project.remove_task(task.id)
    print_success(f"Task '{task.title}' deleted from '{project.title}'.")
    logger.info("Deleted task: %r", task)
    return True


# ── Internal helpers ───────────────────────────────────────────────────────────

def _find_project(title: str, users: list):
    """
    Search across all users' projects for a matching title.
    Returns the first match or None.
    """
    for user in users:
        project = user.get_project_by_title(title)
        if project:
            return project
    print_error(f"Project '{title}' not found.")
    return None
