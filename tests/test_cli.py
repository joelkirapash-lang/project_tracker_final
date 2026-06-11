"""
tests/test_cli.py
Unit tests for CLI command handlers and persistence.
Run with: pytest tests/ -v
"""
import json
import pytest
from pathlib import Path
from unittest.mock import patch
from argparse import Namespace

from models.user import User
from models.project import Project
from models.task import Task
from cli.user_commands import cmd_add_user, cmd_list_users, cmd_update_user, cmd_delete_user
from cli.project_commands import cmd_add_project, cmd_list_projects, cmd_update_project, cmd_delete_project
from cli.task_commands import cmd_add_task, cmd_list_tasks, cmd_complete_task, cmd_update_task, cmd_delete_task
from utils.storage import save_data, load_data


# ── Fixtures ───────────────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def reset_id_counters():
    """Reset class-level ID counters before each test to avoid cross-test pollution."""
    User._id_counter = 1
    Project._id_counter = 1
    Task._id_counter = 1
    yield
    User._id_counter = 1
    Project._id_counter = 1
    Task._id_counter = 1


@pytest.fixture
def sample_users():
    """Return a fresh list with one user, one project, and one task."""
    u = User(name="Alice", email="alice@test.com", role="admin")
    p = Project(title="Alpha Project", due_date="2025-12-01")
    t = Task(title="Write code", status="todo")
    p.add_task(t)
    u.add_project(p)
    return [u]


# ── User command tests ─────────────────────────────────────────────────────────

class TestUserCommands:
    def test_add_user_success(self):
        users = []
        args = Namespace(name="Bob", email="bob@test.com", role="member")
        result = cmd_add_user(args, users)
        assert result is True
        assert len(users) == 1
        assert users[0].name == "Bob"

    def test_add_user_duplicate_fails(self, sample_users):
        args = Namespace(name="Alice", email="", role="member")
        result = cmd_add_user(args, sample_users)
        assert result is False
        assert len(sample_users) == 1  # no new user

    def test_add_user_invalid_email_fails(self):
        users = []
        args = Namespace(name="Bad Email", email="notanemail", role="member")
        result = cmd_add_user(args, users)
        assert result is False

    def test_list_users_no_crash(self, sample_users):
        args = Namespace()
        result = cmd_list_users(args, sample_users)
        assert result is False  # list commands don't modify state

    def test_update_user_name(self, sample_users):
        args = Namespace(name="Alice", new_name="Alicia", email=None, role=None)
        result = cmd_update_user(args, sample_users)
        assert result is True
        assert sample_users[0].name == "Alicia"

    def test_update_user_not_found(self, sample_users):
        args = Namespace(name="Nobody", new_name="X", email=None, role=None)
        result = cmd_update_user(args, sample_users)
        assert result is False

    def test_delete_user_success(self, sample_users):
        args = Namespace(name="Alice")
        result = cmd_delete_user(args, sample_users)
        assert result is True
        assert sample_users == []

    def test_delete_user_not_found(self, sample_users):
        args = Namespace(name="Ghost")
        result = cmd_delete_user(args, sample_users)
        assert result is False


# ── Project command tests ──────────────────────────────────────────────────────

class TestProjectCommands:
    def test_add_project_success(self, sample_users):
        args = Namespace(user="Alice", title="New Project", description="", due_date="")
        result = cmd_add_project(args, sample_users)
        assert result is True
        assert len(sample_users[0].projects) == 2

    def test_add_project_duplicate_fails(self, sample_users):
        args = Namespace(user="Alice", title="Alpha Project", description="", due_date="")
        result = cmd_add_project(args, sample_users)
        assert result is False

    def test_add_project_invalid_date_fails(self, sample_users):
        args = Namespace(user="Alice", title="Bad Date Proj", description="", due_date="31/12/2025")
        result = cmd_add_project(args, sample_users)
        assert result is False

    def test_add_project_user_not_found(self, sample_users):
        args = Namespace(user="Nobody", title="Ghost Project", description="", due_date="")
        result = cmd_add_project(args, sample_users)
        assert result is False

    def test_list_projects_no_crash(self, sample_users):
        args = Namespace(user="Alice")
        result = cmd_list_projects(args, sample_users)
        assert result is False

    def test_update_project_title(self, sample_users):
        args = Namespace(
            user="Alice", title="Alpha Project",
            new_title="Beta Project", description=None, due_date=None
        )
        result = cmd_update_project(args, sample_users)
        assert result is True
        assert sample_users[0].projects[0].title == "Beta Project"

    def test_delete_project_success(self, sample_users):
        args = Namespace(user="Alice", title="Alpha Project")
        result = cmd_delete_project(args, sample_users)
        assert result is True
        assert sample_users[0].projects == []


# ── Task command tests ─────────────────────────────────────────────────────────

class TestTaskCommands:
    def test_add_task_success(self, sample_users):
        args = Namespace(project="Alpha Project", title="New Task", assigned_to="", status="todo")
        result = cmd_add_task(args, sample_users)
        assert result is True
        assert len(sample_users[0].projects[0].tasks) == 2

    def test_add_task_duplicate_fails(self, sample_users):
        args = Namespace(project="Alpha Project", title="Write code", assigned_to="", status="todo")
        result = cmd_add_task(args, sample_users)
        assert result is False

    def test_add_task_project_not_found(self, sample_users):
        args = Namespace(project="Ghost Project", title="Invisible Task", assigned_to="", status="todo")
        result = cmd_add_task(args, sample_users)
        assert result is False

    def test_complete_task(self, sample_users):
        args = Namespace(project="Alpha Project", title="Write code")
        result = cmd_complete_task(args, sample_users)
        assert result is True
        task = sample_users[0].projects[0].tasks[0]
        assert task.status == "done"

    def test_complete_already_done(self, sample_users):
        proj = sample_users[0].projects[0]
        proj.tasks[0].complete()
        args = Namespace(project="Alpha Project", title="Write code")
        result = cmd_complete_task(args, sample_users)
        assert result is False  # already done, nothing changed

    def test_update_task_status(self, sample_users):
        args = Namespace(
            project="Alpha Project", title="Write code",
            new_title=None, status="in_progress", assigned_to=None
        )
        result = cmd_update_task(args, sample_users)
        assert result is True
        task = sample_users[0].projects[0].tasks[0]
        assert task.status == "in_progress"

    def test_delete_task(self, sample_users):
        args = Namespace(project="Alpha Project", title="Write code")
        result = cmd_delete_task(args, sample_users)
        assert result is True
        assert sample_users[0].projects[0].tasks == []


# ── Storage tests ──────────────────────────────────────────────────────────────

class TestStorage:
    def test_save_and_load_roundtrip(self, tmp_path, sample_users):
        filepath = tmp_path / "test_data.json"
        save_data(sample_users, filepath)
        loaded = load_data(filepath)

        assert len(loaded) == 1
        assert loaded[0].name == "Alice"
        assert len(loaded[0].projects) == 1
        assert len(loaded[0].projects[0].tasks) == 1
        assert loaded[0].projects[0].tasks[0].title == "Write code"

    def test_load_missing_file_returns_empty(self, tmp_path):
        filepath = tmp_path / "nonexistent.json"
        result = load_data(filepath)
        assert result == []

    def test_load_empty_file_returns_empty(self, tmp_path):
        filepath = tmp_path / "empty.json"
        filepath.write_text("")
        result = load_data(filepath)
        assert result == []

    def test_load_malformed_json_returns_empty(self, tmp_path):
        filepath = tmp_path / "bad.json"
        filepath.write_text("{this is not json}")
        result = load_data(filepath)
        assert result == []

    def test_save_creates_data_directory(self, tmp_path):
        nested = tmp_path / "deep" / "path" / "data.json"
        users = [User(name="Solo")]
        save_data(users, nested)
        assert nested.exists()

    def test_saved_json_is_valid(self, tmp_path, sample_users):
        filepath = tmp_path / "valid.json"
        save_data(sample_users, filepath)
        with open(filepath) as f:
            data = json.load(f)
        assert "users" in data
        assert data["users"][0]["name"] == "Alice"
