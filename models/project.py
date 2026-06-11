"""
models/project.py
Project model — belongs to a User, contains many Tasks.
"""
from datetime import datetime
from models.task import Task


class Project:
    """Represents a project owned by a user, containing multiple tasks."""

    _id_counter = 1  # Class-level ID counter

    def __init__(
        self,
        title: str,
        description: str = "",
        due_date: str = "",
        project_id: int = None,
        created_at: str = None,
    ):
        """Initialize a Project."""
        if project_id is not None:
            self._id = project_id
            if project_id >= Project._id_counter:
                Project._id_counter = project_id + 1
        else:
            self._id = Project._id_counter
            Project._id_counter += 1

        self._title = title
        self._description = description
        self._due_date = due_date
        self._created_at = created_at or datetime.now().isoformat(timespec="seconds")
        self._tasks: list[Task] = []

    # ── Properties ────────────────────────────────────────────────

    @property
    def id(self) -> int:
        """Return the project's unique ID."""
        return self._id

    @property
    def title(self) -> str:
        """Return the project title."""
        return self._title

    @title.setter
    def title(self, value: str):
        """Set the project title with validation."""
        if not value or not value.strip():
            raise ValueError("Project title cannot be empty.")
        self._title = value.strip()

    @property
    def description(self) -> str:
        """Return the project description."""
        return self._description

    @description.setter
    def description(self, value: str):
        """Set the project description."""
        self._description = value or ""

    @property
    def due_date(self) -> str:
        """Return the project due date."""
        return self._due_date

    @due_date.setter
    def due_date(self, value: str):
        """Set and validate the due date (YYYY-MM-DD)."""
        if value:
            try:
                datetime.strptime(value, "%Y-%m-%d")
            except ValueError:
                raise ValueError("due_date must be in YYYY-MM-DD format.")
        self._due_date = value or ""

    @property
    def created_at(self) -> str:
        """Return project creation timestamp."""
        return self._created_at

    @property
    def tasks(self) -> list:
        """Return the list of tasks for this project."""
        return list(self._tasks)

    # ── Task management ────────────────────────────────────────────

    def add_task(self, task: Task):
        """Add a Task object to this project."""
        if not isinstance(task, Task):
            raise TypeError("Expected a Task instance.")
        self._tasks.append(task)

    def get_task_by_id(self, task_id: int) -> Task | None:
        """Retrieve a task by its ID."""
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def get_task_by_title(self, title: str) -> Task | None:
        """Retrieve a task by its title (case-insensitive)."""
        for task in self._tasks:
            if task.title.lower() == title.lower():
                return task
        return None

    def remove_task(self, task_id: int) -> bool:
        """Remove a task by ID. Returns True if removed."""
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                self._tasks.pop(i)
                return True
        return False

    def pending_tasks(self) -> list:
        """Return tasks that are not done."""
        return [t for t in self._tasks if t.status != "done"]

    def completed_tasks(self) -> list:
        """Return tasks that are done."""
        return [t for t in self._tasks if t.status == "done"]

    # ── Serialization ──────────────────────────────────────────────

    def to_dict(self) -> dict:
        """Serialize project to a dictionary for JSON persistence."""
        return {
            "id": self._id,
            "title": self._title,
            "description": self._description,
            "due_date": self._due_date,
            "created_at": self._created_at,
            "tasks": [t.to_dict() for t in self._tasks],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Project":
        """Deserialize a Project from a dictionary."""
        project = cls(
            title=data["title"],
            description=data.get("description", ""),
            due_date=data.get("due_date", ""),
            project_id=data.get("id"),
            created_at=data.get("created_at"),
        )
        for task_data in data.get("tasks", []):
            project.add_task(Task.from_dict(task_data))
        return project

    def __str__(self) -> str:
        due = f" (due: {self._due_date})" if self._due_date else ""
        task_count = len(self._tasks)
        done_count = len(self.completed_tasks())
        return (
            f"[{self._id}] {self._title}{due} "
            f"— {done_count}/{task_count} tasks done"
        )

    def __repr__(self) -> str:
        return f"Project(id={self._id}, title={self._title!r})"
