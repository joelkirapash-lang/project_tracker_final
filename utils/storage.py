"""
utils/storage.py
Handles loading and saving all data to/from JSON files.
Full persistence with error handling and clean load/save structure.
"""
import json
import logging
import os
from pathlib import Path

from models.user import User

logger = logging.getLogger(__name__)

# Default data directory and file path
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_FILE = DATA_DIR / "tracker_data.json"


def ensure_data_dir():
    """Create the data directory if it doesn't exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def save_data(users: list[User], filepath: Path = DATA_FILE) -> None:
    """
    Persist all users (with their projects and tasks) to a JSON file.

    Args:
        users: List of User objects to serialize.
        filepath: Path to the JSON output file.
    """
    ensure_data_dir()
    filepath.parent.mkdir(parents=True, exist_ok=True)
    data = {"users": [u.to_dict() for u in users]}
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.debug("Data saved to %s", filepath)
    except OSError as exc:
        logger.error("Failed to save data: %s", exc)
        raise


def load_data(filepath: Path = DATA_FILE) -> list[User]:
    """
    Load all users (with their projects and tasks) from a JSON file.

    Args:
        filepath: Path to the JSON data file.

    Returns:
        List of User objects. Returns an empty list if the file is missing.
    """
    if not filepath.exists():
        logger.debug("Data file not found at %s — starting fresh.", filepath)
        return []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            raw = f.read().strip()
            if not raw:
                return []
            data = json.loads(raw)
        users = [User.from_dict(u) for u in data.get("users", [])]
        logger.debug("Loaded %d user(s) from %s", len(users), filepath)
        return users
    except json.JSONDecodeError as exc:
        logger.error("Malformed JSON in %s: %s", filepath, exc)
        return []
    except (KeyError, TypeError) as exc:
        logger.error("Data structure error in %s: %s", filepath, exc)
        return []
    except OSError as exc:
        logger.error("Cannot read file %s: %s", filepath, exc)
        return []


def backup_data(filepath: Path = DATA_FILE) -> Path | None:
    """
    Create a timestamped backup of the data file before overwriting.

    Returns:
        Path to the backup file, or None if no backup was needed.
    """
    if not filepath.exists():
        return None
    from datetime import datetime

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = filepath.with_suffix(f".{timestamp}.bak.json")
    try:
        import shutil

        shutil.copy2(filepath, backup_path)
        logger.debug("Backup created at %s", backup_path)
        return backup_path
    except OSError as exc:
        logger.warning("Could not create backup: %s", exc)
        return None
