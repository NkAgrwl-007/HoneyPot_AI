import json
import hashlib
import os

USERS_FILE = "data/users.json"

def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    """Load users from the JSON file, or return empty dict if error"""
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}

def save_users(users):
    """Save users dictionary to the JSON file"""
    try:
        with open(USERS_FILE, "w") as f:
            json.dump(users, f, indent=4)
    except IOError as e:
        print(f"[ERROR] Failed to save users: {e}")

def authenticate_user(username, password):
    """Check if the given credentials match a registered user"""
    users = load_users()
    hashed = hash_password(password)
    if users.get(username) == hashed:
        return True  # Correct password
    return False  # Incorrect password

def register_user(username, password):
    """Register a new user if the username is not taken and inputs are valid"""
    if not username or not password:
        return "❌ Username or password cannot be empty."  # Invalid input
    
    users = load_users()
    if username in users:
        return "❌ Username already exists."  # User already exists
    
    # Register the user
    users[username] = hash_password(password)
    save_users(users)
    return "✅ Account created successfully!"

def get_all_users():
    """Return the list of all registered usernames (for debugging or admin use)"""
    users = load_users()
    return list(users.keys())
