# 📋 Project Tracker CLI

A Python-based Command-Line Interface (CLI) tool for managing users, projects, and tasks. Built with clean OOP design, JSON persistence, and a rich terminal UI.

---

## ✨ Features

- **User management** — create, list, update, and delete users with roles (`admin` / `member`)
- **Project management** — add projects to users, track due dates and descriptions
- **Task management** — add tasks to projects, assign them, update status, and mark as complete
- **Rich CLI output** — colour-coded tables and status indicators via the `rich` package
- **JSON persistence** — all data is automatically saved to `data/tracker_data.json`
- **Full test suite** — pytest tests for models, CLI commands, and storage

---

## 🗂️ Project Structure

```
project_tracker/
├── main.py               # CLI entry point (argparse)
├── requirements.txt      # pip dependencies
├── Pipfile               # pipenv dependencies
├── .gitignore
├── README.md
│
├── models/               # OOP data models
│   ├── __init__.py
│   ├── person.py         # Base Person class
│   ├── user.py           # User (extends Person) → owns Projects
│   ├── project.py        # Project → owns Tasks
│   └── task.py           # Task (leaf node)
│
├── cli/                  # CLI command handlers
│   ├── __init__.py
│   ├── user_commands.py
│   ├── project_commands.py
│   └── task_commands.py
│
├── utils/                # Helpers and utilities
│   ├── __init__.py
│   ├── storage.py        # JSON load/save with error handling
│   ├── display.py        # Rich-powered table displays
│   └── validators.py     # Input validation helpers
│
├── data/                 # Auto-generated JSON storage
│   └── tracker_data.json (created on first run)
│
└── tests/                # pytest test suite
    ├── conftest.py
    ├── test_models.py
    └── test_cli.py
```

---

## ⚙️ Setup Instructions

### Prerequisites
- Python 3.10 or higher
- pip or pipenv

### Option A — pip (recommended for quick start)

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/project-tracker-cli.git
cd project-tracker-cli

# 2. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the CLI
python main.py --help
```

### Option B — pipenv

```bash
git clone https://github.com/<your-username>/project-tracker-cli.git
cd project-tracker-cli

pipenv install
pipenv shell

python main.py --help
```

---

## 🚀 CLI Commands

Every command starts with `python main.py <command> [options]`.

### User Commands

| Command | Description |
|---|---|
| `add-user` | Create a new user |
| `list-users` | List all users |
| `update-user` | Update a user's name, email, or role |
| `delete-user` | Delete a user and all their projects/tasks |

```bash
# Add a user
python main.py add-user --name "Alex" --email "alex@dev.com" --role admin

# List all users
python main.py list-users

# Update a user
python main.py update-user --name "Alex" --new-name "Alexander" --email "alex@new.com"

# Delete a user
python main.py delete-user --name "Alexander"
```

### Project Commands

| Command | Description |
|---|---|
| `add-project` | Add a project to a user |
| `list-projects` | List all projects (or filter by user) |
| `update-project` | Update title, description, or due date |
| `delete-project` | Delete a project and all its tasks |

```bash
# Add a project
python main.py add-project --user "Alex" --title "CLI Tool" --description "Build a tracker" --due-date 2025-12-31

# List all projects
python main.py list-projects

# List projects for a specific user
python main.py list-projects --user "Alex"

# Update a project
python main.py update-project --user "Alex" --title "CLI Tool" --new-title "Tracker v2" --due-date 2026-01-15

# Delete a project
python main.py delete-project --user "Alex" --title "Tracker v2"
```

### Task Commands

| Command | Description |
|---|---|
| `add-task` | Add a task to a project |
| `list-tasks` | List all tasks in a project |
| `complete-task` | Mark a task as done |
| `update-task` | Update title, status, or assignee |
| `delete-task` | Delete a task from a project |

```bash
# Add a task
python main.py add-task --project "CLI Tool" --title "Implement add-task" --assigned-to "Alex"

# List tasks
python main.py list-tasks --project "CLI Tool"

# Complete a task
python main.py complete-task --project "CLI Tool" --title "Implement add-task"

# Update a task
python main.py update-task --project "CLI Tool" --title "Implement add-task" --status in_progress

# Delete a task
python main.py delete-task --project "CLI Tool" --title "Implement add-task"
```

### Verbose / Debug Mode

Add `--verbose` or `-v` to any command to enable debug logging:

```bash
python main.py --verbose list-users
```

---

## 🧪 Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ -v --cov=. --cov-report=term-missing

# Run a specific test file
pytest tests/test_models.py -v
pytest tests/test_cli.py -v
```

---

## 🏗️ OOP Design Overview

```
Person (base class)
└── User (inherits name, email from Person)
    └── projects: list[Project]  ← one-to-many
        └── Project
            └── tasks: list[Task]  ← one-to-many
                └── Task
```

Key design patterns used:
- **Inheritance**: `User` extends `Person`
- **Encapsulation**: `@property` / `@setter` on all attributes with validation
- **Class attributes**: `_id_counter` auto-increments IDs on every model
- **Serialization**: every model has `to_dict()` and `from_dict()` for JSON persistence

---

## 📦 External Packages

| Package | Version | Usage |
|---|---|---|
| `rich` | ≥13.0 | Colour-coded tables, panels, and status messages |
| `python-dateutil` | ≥2.8.2 | Flexible date parsing utilities |
| `pytest` | ≥7.0 | Unit testing framework |

---

## 💾 Data Persistence

All data is stored in `data/tracker_data.json`. The file is auto-created on first use. Example structure:

```json
{
  "users": [
    {
      "id": 1,
      "name": "Alex",
      "email": "alex@dev.com",
      "role": "admin",
      "created_at": "2025-06-09T10:00:00",
      "projects": [
        {
          "id": 1,
          "title": "CLI Tool",
          "description": "Build a tracker",
          "due_date": "2025-12-31",
          "tasks": [
            {
              "id": 1,
              "title": "Implement add-task",
              "status": "done",
              "assigned_to": "Alex"
            }
          ]
        }
      ]
    }
  ]
}
```

---

## 🔧 Known Issues / Limitations

- Project titles are searched **globally** across all users. If two users have a project with the same title, `add-task` and `list-tasks` will match the first one found. A future improvement would add `--user` flags to task commands.
- The backup system (`utils/storage.py::backup_data`) is available but not wired into the CLI by default. You can call it manually before bulk operations.

---

## 📝 Git Workflow

This project follows a feature-branch workflow:

```
main          ← stable, submission-ready
├── feature/models       ← OOP model classes
├── feature/cli          ← CLI commands
├── feature/persistence  ← JSON storage
└── feature/tests        ← test suite
```

Commit with meaningful messages, e.g.:
```
git commit -m "feat: add Task model with status validation"
git commit -m "feat: add complete-task CLI subcommand"
git commit -m "test: add storage roundtrip tests"
```
