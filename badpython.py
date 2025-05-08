# BAD PRACTICE - DO NOT USE IN REAL APPLICATIONS
def connect_to_database():
    username = "admin"
    # Bad practice: Hardcoded clear text password
    password = "SuperSecret123!"

    database_url = "postgresql://localhost:5432/mydb"

    print(f"Connecting to database as {username}")
    # In a real application, this would use the password to authenticate
    connection = f"Connected to {database_url} with credentials {username}:{password}"
    return connection

def get_user_data(user_id):
    connection = connect_to_database()
    # This would normally query the database
    print(f"Fetching data for user {user_id}")
    return {"id": user_id, "name": "Test User"}

# Usage
result = get_user_data(42)
print(result)
