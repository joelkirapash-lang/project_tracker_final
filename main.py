#!/usr/bin/env python3
"""
main.py
Entry point for the Project Tracker CLI.

Usage examples:
    python main.py add-user --name "Alex" --email "alex@example.com"
    python main.py add-project --user "Alex" --title "CLI Tool" --due-date 2025-12-31
    python main.py add-task --project "CLI Tool" --title "Implement add-task"
    python main.py list-users
    python main.py list-projects --user "Alex"
    python main.py list-tasks --project "CLI Tool"
    python main.py complete-task --project "CLI Tool" --title "Implement add-task"
"""

import argparse
import logging
import sys

from utils.storage import load_data, save_data
from utils.display import display_banner, print_error
from cli.user_commands import (
    cmd_add_user,
    cmd_list_users,
    cmd_update_user,
    cmd_delete_user,
)
from cli.project_commands import (
    cmd_add_project,
    cmd_list_projects,
    cmd_update_project,
    cmd_delete_project,
)
from cli.task_commands import (
    cmd_add_task,
    cmd_list_tasks,
    cmd_complete_task,
    cmd_update_task,
    cmd_delete_task,
)

# ── Logging setup ──────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)


# ── Parser builder ─────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    """Build and return the top-level argument parser with all subcommands."""

    parser = argparse.ArgumentParser(
        prog="tracker",
        description="📋 Project Tracker CLI — manage users, projects, and tasks.",
        epilog="Run 'tracker <command> --help' for command-specific help.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose/debug logging output.",
    )

    subparsers = parser.add_subparsers(dest="command", metavar="<command>")
    subparsers.required = True

    # ── User commands ──────────────────────────────────────────────

    # add-user
    p_add_user = subparsers.add_parser("add-user", help="Create a new user.")
    p_add_user.add_argument("--name", required=True, help="User's full name.")
    p_add_user.add_argument("--email", default="", help="User's email address.")
    p_add_user.add_argument(
        "--role", default="member", choices=["admin", "member"],
        help="User role (default: member)."
    )

    # list-users
    subparsers.add_parser("list-users", help="List all users.")

    # update-user
    p_upd_user = subparsers.add_parser("update-user", help="Update an existing user.")
    p_upd_user.add_argument("--name", required=True, help="Current name of the user.")
    p_upd_user.add_argument("--new-name", default=None, help="New name.")
    p_upd_user.add_argument("--email", default=None, help="New email.")
    p_upd_user.add_argument("--role", default=None, choices=["admin", "member"], help="New role.")

    # delete-user
    p_del_user = subparsers.add_parser("delete-user", help="Delete a user and all their data.")
    p_del_user.add_argument("--name", required=True, help="Name of the user to delete.")

    # ── Project commands ───────────────────────────────────────────

    # add-project
    p_add_proj = subparsers.add_parser("add-project", help="Add a project to a user.")
    p_add_proj.add_argument("--user", required=True, help="Owner's name.")
    p_add_proj.add_argument("--title", required=True, help="Project title.")
    p_add_proj.add_argument("--description", default="", help="Project description.")
    p_add_proj.add_argument("--due-date", default="", dest="due_date", help="Due date (YYYY-MM-DD).")

    # list-projects
    p_list_proj = subparsers.add_parser("list-projects", help="List projects (all or by user).")
    p_list_proj.add_argument("--user", default=None, help="Filter by user name.")

    # update-project
    p_upd_proj = subparsers.add_parser("update-project", help="Update a project's details.")
    p_upd_proj.add_argument("--user", required=True, help="Owner's name.")
    p_upd_proj.add_argument("--title", required=True, help="Current project title.")
    p_upd_proj.add_argument("--new-title", default=None, dest="new_title", help="New title.")
    p_upd_proj.add_argument("--description", default=None, help="New description.")
    p_upd_proj.add_argument("--due-date", default=None, dest="due_date", help="New due date (YYYY-MM-DD).")

    # delete-project
    p_del_proj = subparsers.add_parser("delete-project", help="Delete a project.")
    p_del_proj.add_argument("--user", required=True, help="Owner's name.")
    p_del_proj.add_argument("--title", required=True, help="Project title to delete.")

    # ── Task commands ──────────────────────────────────────────────

    # add-task
    p_add_task = subparsers.add_parser("add-task", help="Add a task to a project.")
    p_add_task.add_argument("--project", required=True, help="Project title.")
    p_add_task.add_argument("--title", required=True, help="Task title.")
    p_add_task.add_argument("--assigned-to", default="", dest="assigned_to", help="Assign to a person.")
    p_add_task.add_argument(
        "--status", default="todo", choices=["todo", "in_progress", "done"],
        help="Initial status (default: todo)."
    )

    # list-tasks
    p_list_tasks = subparsers.add_parser("list-tasks", help="List all tasks in a project.")
    p_list_tasks.add_argument("--project", required=True, help="Project title.")

    # complete-task
    p_complete = subparsers.add_parser("complete-task", help="Mark a task as done.")
    p_complete.add_argument("--project", required=True, help="Project title.")
    p_complete.add_argument("--title", required=True, help="Task title.")

    # update-task
    p_upd_task = subparsers.add_parser("update-task", help="Update a task's details.")
    p_upd_task.add_argument("--project", required=True, help="Project title.")
    p_upd_task.add_argument("--title", required=True, help="Current task title.")
    p_upd_task.add_argument("--new-title", default=None, dest="new_title", help="New title.")
    p_upd_task.add_argument(
        "--status", default=None, choices=["todo", "in_progress", "done"],
        help="New status."
    )
    p_upd_task.add_argument("--assigned-to", default=None, dest="assigned_to", help="New assignee.")

    # delete-task
    p_del_task = subparsers.add_parser("delete-task", help="Delete a task from a project.")
    p_del_task.add_argument("--project", required=True, help="Project title.")
    p_del_task.add_argument("--title", required=True, help="Task title to delete.")

    return parser


# ── Command dispatch ───────────────────────────────────────────────────────────

COMMAND_MAP = {
    "add-user":       cmd_add_user,
    "list-users":     cmd_list_users,
    "update-user":    cmd_update_user,
    "delete-user":    cmd_delete_user,
    "add-project":    cmd_add_project,
    "list-projects":  cmd_list_projects,
    "update-project": cmd_update_project,
    "delete-project": cmd_delete_project,
    "add-task":       cmd_add_task,
    "list-tasks":     cmd_list_tasks,
    "complete-task":  cmd_complete_task,
    "update-task":    cmd_update_task,
    "delete-task":    cmd_delete_task,
}


def main():
    """Main entry point: parse args, load data, dispatch command, save if modified."""
    display_banner()

    parser = build_parser()
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Load persisted data
    users = load_data()

    # Dispatch to the correct handler
    handler = COMMAND_MAP.get(args.command)
    if handler is None:
        print_error(f"Unknown command: '{args.command}'")
        sys.exit(1)

    try:
        modified = handler(args, users)
    except (ValueError, TypeError) as exc:
        print_error(str(exc))
        sys.exit(1)

    # Persist changes only when data was modified
    if modified:
        save_data(users)


if __name__ == "__main__":
    main()
