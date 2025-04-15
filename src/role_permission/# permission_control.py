# permission_control.py

class Role:
    def __init__(self, role_name, permissions=None):
        if permissions is None:
            permissions = []
        self.role_name = role_name
        self.permissions = permissions

    def add_permission(self, permission):
        if permission not in self.permissions:
            self.permissions.append(permission)

    def remove_permission(self, permission):
        if permission in self.permissions:
            self.permissions.remove(permission)

    def __str__(self):
        return f"Role: {self.role_name} | Permissions: {', '.join(self.permissions)}"

class User:
    def __init__(self, user_id, username, role=None):
        self.user_id = user_id
        self.username = username
        self.role = role if role else Role("Guest")

    def assign_role(self, role):
        self.role = role

    def __str__(self):
        return f"User: {self.username} | Role: {self.role.role_name} | Permissions: {', '.join(self.role.permissions)}"

class PermissionManager:
    def __init__(self):
        self.roles = {}
        self.users = {}

    def create_role(self, role_name, permissions=None):
        role = Role(role_name, permissions)
        self.roles[role_name] = role
        return role

    def assign_role_to_user(self, user_id, role_name):
        if user_id not in self.users:
            raise KeyError(f"User {user_id} not found.")
        if role_name not in self.roles:
            raise KeyError(f"Role {role_name} not found.")
        user = self.users[user_id]
        role = self.roles[role_name]
        user.assign_role(role)

    def add_permission_to_role(self, role_name, permission):
        if role_name in self.roles:
            role = self.roles[role_name]
            role.add_permission(permission)
        else:
            raise KeyError(f"Role {role_name} not found.")

    def remove_permission_from_role(self, role_name, permission):
        if role_name in self.roles:
            role = self.roles[role_name]
            role.remove_permission(permission)
        else:
            raise KeyError(f"Role {role_name} not found.")

    def add_user(self, user_id, username, role_name="Guest"):
        if role_name not in self.roles:
            raise KeyError(f"Role {role_name} not found.")
        role = self.roles[role_name]
        user = User(user_id, username, role)
        self.users[user_id] = user
        return user

    def get_user(self, user_id):
        return self.users.get(user_id)

    def list_all_users(self):
        return list(self.users.values())

# Sample usage
if __name__ == "__main__":
    manager = PermissionManager()

    # Create roles
    admin_role = manager.create_role("Admin", permissions=["view", "edit", "delete"])
    user_role = manager.create_role("User", permissions=["view", "edit"])

    # Add users
    user1 = manager.add_user("001", "alice", "Admin")
    user2 = manager.add_user("002", "bob", "User")

    # Assign role to user
    print("--- User Roles ---")
    for user in manager.list_all_users():
        print(user)

    # Add and remove permissions from roles
    manager.add_permission_to_role("User", "comment")
    manager.remove_permission_from_role("Admin", "delete")

    print("\n--- Updated User Roles ---")
    for user in manager.list_all_users():
        print(user)

    # Assign new role to user
    manager.assign_role_to_user("002", "Admin")
    print("\n--- After Role Update ---")
    for user in manager.list_all_users():
        print(user)
