"""
models/user.py
User model — inherits from Person, owns many Projects.
Demonstrates inheritance, encapsulation, and one-to-many relationships.
"""
from models.person import Person
from models.project import Project


class User(Person):
    """
    A User is a Person who owns Projects.
    Inherits name and email from Person.
    """

    _id_counter = 1  # Class-level ID counter shared across all User instances

    def __init__(
        self,
        name: str,
        email: str = "",
        role: str = "member",
        user_id: int = None,
        created_at: str = None,
    ):
        """Initialize a User, calling the parent Person constructor."""
        from datetime import datetime

        super().__init__(name, email)

        if user_id is not None:
            self._id = user_id
            if user_id >= User._id_counter:
                User._id_counter = user_id + 1
        else:
            self._id = User._id_counter
            User._id_counter += 1

        self._role = role
        self._created_at = created_at or datetime.now().isoformat(timespec="seconds")
        self._projects: list[Project] = []

    # ── Properties ────────────────────────────────────────────────

    @property
    def id(self) -> int:
        """Return the user's unique ID."""
        return self._id

    @property
    def role(self) -> str:
        """Return the user's role."""
        return self._role

    @role.setter
    def role(self, value: str):
        """Set the user's role."""
        valid = ("admin", "member")
        if value not in valid:
            raise ValueError(f"Role must be one of: {', '.join(valid)}")
        self._role = value

    @property
    def created_at(self) -> str:
        """Return the user creation timestamp."""
        return self._created_at

    @property
    def projects(self) -> list:
        """Return a copy of the user's project list."""
        return list(self._projects)

    # ── Project management ─────────────────────────────────────────

    def add_project(self, project: Project):
        """Add a Project to this user."""
        if not isinstance(project, Project):
            raise TypeError("Expected a Project instance.")
        self._projects.append(project)

    def get_project_by_title(self, title: str) -> Project | None:
        """Find a project by title (case-insensitive)."""
        for project in self._projects:
            if project.title.lower() == title.lower():
                return project
        return None

    def get_project_by_id(self, project_id: int) -> Project | None:
        """Find a project by its ID."""
        for project in self._projects:
            if project.id == project_id:
                return project
        return None

    def remove_project(self, project_id: int) -> bool:
        """Remove a project by ID. Returns True if removed."""
        for i, project in enumerate(self._projects):
            if project.id == project_id:
                self._projects.pop(i)
                return True
        return False

    # ── Serialization ──────────────────────────────────────────────

    def to_dict(self) -> dict:
        """Serialize user to a dictionary for JSON persistence."""
        return {
            "id": self._id,
            "name": self._name,
            "email": self._email,
            "role": self._role,
            "created_at": self._created_at,
            "projects": [p.to_dict() for p in self._projects],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        """Deserialize a User from a dictionary."""
        user = cls(
            name=data["name"],
            email=data.get("email", ""),
            role=data.get("role", "member"),
            user_id=data.get("id"),
            created_at=data.get("created_at"),
        )
        for project_data in data.get("projects", []):
            user.add_project(Project.from_dict(project_data))
        return user

    def __str__(self) -> str:
        email_str = f" <{self._email}>" if self._email else ""
        return (
            f"[{self._id}] {self._name}{email_str} "
            f"({self._role}) — {len(self._projects)} project(s)"
        )

    def __repr__(self) -> str:
        return f"User(id={self._id}, name={self._name!r}, role={self._role!r})"
