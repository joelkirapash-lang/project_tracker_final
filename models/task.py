"""
models/task.py
Task model — belongs to a Project.
Supports status tracking and assignment.
"""
from datetime import datetime


class Task:
    """Represents a task within a project."""

    _id_counter = 1  # Class-level ID counter

    VALID_STATUSES = ("todo", "in_progress", "done")

    def __init__(
        self,
        title: str,
        status: str = "todo",
        assigned_to: str = "",
        task_id: int = None,
        created_at: str = None,
    ):
        """Initialize a Task."""
        if task_id is not None:
            self._id = task_id
            # Keep counter ahead of loaded IDs to avoid collisions
            if task_id >= Task._id_counter:
                Task._id_counter = task_id + 1
        else:
            self._id = Task._id_counter
            Task._id_counter += 1

        if not title or not str(title).strip():
            raise ValueError("Task title cannot be empty.")
        self._title = title.strip()
        self.status = status  # uses the setter for validation
        self._assigned_to = assigned_to
        self._created_at = created_at or datetime.now().isoformat(timespec="seconds")

    # ── Properties ────────────────────────────────────────────────

    @property
    def id(self) -> int:
        """Return the task's unique ID."""
        return self._id

    @property
    def title(self) -> str:
        """Return the task title."""
        return self._title

    @title.setter
    def title(self, value: str):
        """Set the task title with validation."""
        if not value or not str(value).strip():
            raise ValueError("Task title cannot be empty.")
        self._title = value.strip()

    @property
    def status(self) -> str:
        """Return the task status."""
        return self._status

    @status.setter
    def status(self, value: str):
        """Set task status; must be one of the valid statuses."""
        if value not in self.VALID_STATUSES:
            raise ValueError(
                f"Invalid status '{value}'. Choose from: {', '.join(self.VALID_STATUSES)}"
            )
        self._status = value

    @property
    def assigned_to(self) -> str:
        """Return who the task is assigned to."""
        return self._assigned_to

    @assigned_to.setter
    def assigned_to(self, value: str):
        """Assign the task to a person."""
        self._assigned_to = value or ""

    @property
    def created_at(self) -> str:
        """Return the task creation timestamp."""
        return self._created_at

    # ── Instance methods ───────────────────────────────────────────

    def complete(self):
        """Mark the task as done."""
        self._status = "done"

    def to_dict(self) -> dict:
        """Serialize task to a dictionary for JSON persistence."""
        return {
            "id": self._id,
            "title": self._title,
            "status": self._status,
            "assigned_to": self._assigned_to,
            "created_at": self._created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Deserialize a Task from a dictionary."""
        return cls(
            title=data["title"],
            status=data.get("status", "todo"),
            assigned_to=data.get("assigned_to", ""),
            task_id=data.get("id"),
            created_at=data.get("created_at"),
        )

    def __str__(self) -> str:
        assignee = f" → {self._assigned_to}" if self._assigned_to else ""
        return f"[{self._id}] {self._title} ({self._status}){assignee}"

    def __repr__(self) -> str:
        return f"Task(id={self._id}, title={self._title!r}, status={self._status!r})"
