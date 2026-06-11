"""
utils/display.py
Rich-powered display helpers for pretty-printing tables and panels.
Uses the 'rich' external package for enhanced CLI output.
"""
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from rich.text import Text

console = Console()


def print_success(message: str):
    """Print a green success message."""
    console.print(f"[bold green]✔ {message}[/bold green]")


def print_error(message: str):
    """Print a red error message."""
    console.print(f"[bold red]✖ {message}[/bold red]")


def print_warning(message: str):
    """Print a yellow warning message."""
    console.print(f"[bold yellow]⚠ {message}[/bold yellow]")


def print_info(message: str):
    """Print a cyan informational message."""
    console.print(f"[cyan]{message}[/cyan]")


def display_users(users: list) -> None:
    """Render a rich table of all users."""
    if not users:
        print_warning("No users found.")
        return

    table = Table(
        title="👥 Users",
        box=box.ROUNDED,
        header_style="bold magenta",
        show_lines=True,
    )
    table.add_column("ID", style="dim", width=5, justify="right")
    table.add_column("Name", style="bold white")
    table.add_column("Email", style="cyan")
    table.add_column("Role", style="yellow")
    table.add_column("Projects", justify="center")
    table.add_column("Created", style="dim")

    for u in users:
        table.add_row(
            str(u.id),
            u.name,
            u.email or "—",
            u.role,
            str(len(u.projects)),
            u.created_at[:10],
        )

    console.print(table)


def display_projects(projects: list, owner_name: str = "") -> None:
    """Render a rich table of projects."""
    if not projects:
        print_warning(
            f"No projects found{f' for {owner_name}' if owner_name else ''}."
        )
        return

    title = f"📁 Projects{f' — {owner_name}' if owner_name else ''}"
    table = Table(
        title=title,
        box=box.ROUNDED,
        header_style="bold blue",
        show_lines=True,
    )
    table.add_column("ID", style="dim", width=5, justify="right")
    table.add_column("Title", style="bold white")
    table.add_column("Description", style="white", max_width=35)
    table.add_column("Due Date", style="yellow", justify="center")
    table.add_column("Tasks", justify="center")
    table.add_column("Done", justify="center")

    for p in projects:
        done = len(p.completed_tasks())
        total = len(p.tasks)
        done_style = "green" if done == total and total > 0 else "red"
        table.add_row(
            str(p.id),
            p.title,
            p.description or "—",
            p.due_date or "—",
            str(total),
            Text(f"{done}/{total}", style=done_style),
        )

    console.print(table)


def display_tasks(tasks: list, project_title: str = "") -> None:
    """Render a rich table of tasks."""
    if not tasks:
        print_warning(
            f"No tasks found{f' in \"{project_title}\"' if project_title else ''}."
        )
        return

    status_colors = {"todo": "red", "in_progress": "yellow", "done": "green"}
    title = f"✅ Tasks{f' — {project_title}' if project_title else ''}"

    table = Table(
        title=title,
        box=box.ROUNDED,
        header_style="bold cyan",
        show_lines=True,
    )
    table.add_column("ID", style="dim", width=5, justify="right")
    table.add_column("Title", style="bold white")
    table.add_column("Status", justify="center")
    table.add_column("Assigned To", style="cyan")
    table.add_column("Created", style="dim")

    for t in tasks:
        color = status_colors.get(t.status, "white")
        table.add_row(
            str(t.id),
            t.title,
            Text(t.status, style=f"bold {color}"),
            t.assigned_to or "—",
            t.created_at[:10],
        )

    console.print(table)


def display_banner():
    """Show a welcome banner when the CLI starts."""
    banner = Panel(
        "[bold cyan]Project Tracker CLI[/bold cyan]\n"
        "[dim]Manage users, projects, and tasks from the command line.[/dim]",
        border_style="bright_blue",
        padding=(1, 4),
    )
    console.print(banner)
