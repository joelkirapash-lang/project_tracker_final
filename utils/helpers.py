

def remove_user(users, name):
    """Remove a user by name. Returns True if removed, False if not found."""
    user = find_user(users, name)
    if user:
        users.remove(user)
        return True
    return False
