# attendance_policy.py

class AttendancePolicy:
    def __init__(self, policy_name, max_hours_per_day, min_hours_per_day, overtime_rate):
        self.policy_name = policy_name
        self.max_hours_per_day = max_hours_per_day
        self.min_hours_per_day = min_hours_per_day
        self.overtime_rate = overtime_rate

    def update_policy(self, max_hours=None, min_hours=None, overtime_rate=None):
        if max_hours is not None:
            self.max_hours_per_day = max_hours
        if min_hours is not None:
            self.min_hours_per_day = min_hours
        if overtime_rate is not None:
            self.overtime_rate = overtime_rate

    def __str__(self):
        return f"{self.policy_name}: Max Hours={self.max_hours_per_day}, Min Hours={self.min_hours_per_day}, Overtime Rate={self.overtime_rate}"

class AttendanceManager:
    def __init__(self):
        self.policies = {}

    def add_policy(self, policy_name, max_hours, min_hours, overtime_rate):
        if policy_name in self.policies:
            raise ValueError(f"Policy {policy_name} already exists.")
        self.policies[policy_name] = AttendancePolicy(policy_name, max_hours, min_hours, overtime_rate)

    def get_policy(self, policy_name):
        return self.policies.get(policy_name)

    def update_policy(self, policy_name, max_hours=None, min_hours=None, overtime_rate=None):
        policy = self.get_policy(policy_name)
        if policy:
            policy.update_policy(max_hours, min_hours, overtime_rate)
        else:
            raise KeyError(f"Policy {policy_name} not found.")

    def list_all_policies(self):
        return list(self.policies.values())

    def export_to_dict(self):
        return {
            policy_name: {
                "max_hours": policy.max_hours_per_day,
                "min_hours": policy.min_hours_per_day,
                "overtime_rate": policy.overtime_rate,
            }
            for policy_name, policy in self.policies.items()
        }

    def import_from_dict(self, data):
        for policy_name, info in data.items():
            policy = AttendancePolicy(policy_name, info['max_hours'], info['min_hours'], info['overtime_rate'])
            self.policies[policy_name] = policy

# Sample usage
if __name__ == "__main__":
    manager = AttendanceManager()
    manager.add_policy("Full Time", 8, 4, 1.5)
    manager.add_policy("Part Time", 4, 2, 1.2)

    print("--- All Policies ---")
    for policy in manager.list_all_policies():
        print(policy)

    print("\n--- Policy Update ---")
    manager.update_policy("Full Time", overtime_rate=2)
    for policy in manager.list_all_policies():
        print(policy)
