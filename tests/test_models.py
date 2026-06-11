"""
tests/test_models.py
Unit tests for User, Project, and Task models.
Run with: pytest tests/ -v
"""
import pytest
from models.task import Task
from models.project import Project
from models.user import User
from models.person import Person


# ── Task tests ─────────────────────────────────────────────────────────────────

class TestTask:
    def test_task_creation_defaults(self):
        task = Task(title="Write tests")
        assert task.title == "Write tests"
        assert task.status == "todo"
        assert task.assigned_to == ""
        assert task.id is not None

    def test_task_complete(self):
        task = Task(title="Deploy app")
        task.complete()
        assert task.status == "done"

    def test_task_invalid_status_raises(self):
        with pytest.raises(ValueError):
            Task(title="Bad task", status="flying")

    def test_task_status_setter_valid(self):
        task = Task(title="Go live")
        task.status = "in_progress"
        assert task.status == "in_progress"

    def test_task_empty_title_raises(self):
        with pytest.raises(ValueError):
            Task(title="")

    def test_task_serialization_roundtrip(self):
        task = Task(title="Test roundtrip", status="in_progress", assigned_to="Alex")
        data = task.to_dict()
        restored = Task.from_dict(data)
        assert restored.title == task.title
        assert restored.status == task.status
        assert restored.assigned_to == task.assigned_to
        assert restored.id == task.id

    def test_task_str(self):
        task = Task(title="My task", status="todo", assigned_to="Bob")
        assert "My task" in str(task)
        assert "todo" in str(task)


# ── Project tests ──────────────────────────────────────────────────────────────

class TestProject:
    def test_project_creation(self):
        p = Project(title="Alpha", description="First project", due_date="2025-12-31")
        assert p.title == "Alpha"
        assert p.description == "First project"
        assert p.due_date == "2025-12-31"
        assert p.tasks == []

    def test_add_task_to_project(self):
        p = Project(title="Beta")
        t = Task(title="Subtask")
        p.add_task(t)
        assert len(p.tasks) == 1
        assert p.tasks[0].title == "Subtask"

    def test_get_task_by_title(self):
        p = Project(title="Gamma")
        t = Task(title="Find me")
        p.add_task(t)
        found = p.get_task_by_title("Find me")
        assert found is t

    def test_get_task_by_title_case_insensitive(self):
        p = Project(title="Delta")
        t = Task(title="CaseTest")
        p.add_task(t)
        assert p.get_task_by_title("casetest") is t

    def test_remove_task(self):
        p = Project(title="Epsilon")
        t = Task(title="Remove me")
        p.add_task(t)
        result = p.remove_task(t.id)
        assert result is True
        assert p.tasks == []

    def test_completed_tasks_filter(self):
        p = Project(title="Zeta")
        t1 = Task(title="Done one", status="done")
        t2 = Task(title="Pending one")
        p.add_task(t1)
        p.add_task(t2)
        assert len(p.completed_tasks()) == 1
        assert len(p.pending_tasks()) == 1

    def test_project_invalid_date_raises(self):
        p = Project(title="Bad date")
        with pytest.raises(ValueError):
            p.due_date = "31-12-2025"  # wrong format

    def test_project_serialization_roundtrip(self):
        p = Project(title="Persist", description="Test", due_date="2025-06-01")
        p.add_task(Task(title="T1", status="done"))
        p.add_task(Task(title="T2"))
        data = p.to_dict()
        restored = Project.from_dict(data)
        assert restored.title == p.title
        assert restored.description == p.description
        assert len(restored.tasks) == 2

    def test_add_non_task_raises(self):
        p = Project(title="Type check")
        with pytest.raises(TypeError):
            p.add_task("not a task")


# ── User tests ─────────────────────────────────────────────────────────────────

class TestUser:
    def test_user_inherits_person(self):
        u = User(name="Alice", email="alice@test.com")
        assert isinstance(u, Person)
        assert u.name == "Alice"
        assert u.email == "alice@test.com"

    def test_user_default_role(self):
        u = User(name="Bob")
        assert u.role == "member"

    def test_user_invalid_role_raises(self):
        with pytest.raises(ValueError):
            u = User(name="Hacker")
            u.role = "superadmin"

    def test_add_project_to_user(self):
        u = User(name="Carol")
        p = Project(title="Carol's Project")
        u.add_project(p)
        assert len(u.projects) == 1

    def test_get_project_by_title(self):
        u = User(name="Dave")
        p = Project(title="Searchable")
        u.add_project(p)
        assert u.get_project_by_title("Searchable") is p

    def test_remove_project(self):
        u = User(name="Eve")
        p = Project(title="Removable")
        u.add_project(p)
        result = u.remove_project(p.id)
        assert result is True
        assert u.projects == []

    def test_user_serialization_roundtrip(self):
        u = User(name="Frank", email="frank@test.com", role="admin")
        proj = Project(title="Frank's Project", due_date="2025-09-01")
        proj.add_task(Task(title="Task A", status="done"))
        u.add_project(proj)

        data = u.to_dict()
        restored = User.from_dict(data)

        assert restored.name == u.name
        assert restored.email == u.email
        assert restored.role == u.role
        assert len(restored.projects) == 1
        assert len(restored.projects[0].tasks) == 1

    def test_user_empty_name_raises(self):
        with pytest.raises(ValueError):
            u = User(name="Valid")
            u.name = ""
