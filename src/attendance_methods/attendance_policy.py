# attendance_policy.py

import datetime

class AttendancePolicy:
    def __init__(self, policy_name, max_hours_per_day, min_hours_per_day, overtime_rate, work_start, work_end):
        self.policy_name = policy_name
        self.max_hours_per_day = max_hours_per_day
        self.min_hours_per_day = min_hours_per_day
        self.overtime_rate = overtime_rate
        self.work_start = work_start  # format: "09:00"
        self.work_end = work_end      # format: "18:00"
        self.holiday_exceptions = []

    def update_policy(self, max_hours=None, min_hours=None, overtime_rate=None, work_start=None, work_end=None):
        if max_hours is not None:
            self.max_hours_per_day = max_hours
        if min_hours is not None:
            self.min_hours_per_day = min_hours
        if overtime_rate is not None:
            self.overtime_rate = overtime_rate
        if work_start:
            self.work_start = work_start
        if work_end:
            self.work_end = work_end

    def add_holiday_exception(self, date):
        self.holiday_exceptions.append(date)

    def is_work_day(self, date):
        if date.weekday() >= 5 or date in self.holiday_exceptions:
            return False
        return True

    def is_valid_check_in(self, check_in_time):
        start = datetime.datetime.strptime(self.work_start, "%H:%M").time()
        end = datetime.datetime.strptime(self.work_end, "%H:%M").time()
        return start <= check_in_time <= end

    def __str__(self):
        return (f"Policy: {self.policy_name} | Work: {self.work_start}-{self.work_end} | "
                f"Min Hours: {self.min_hours_per_day} | Max Hours: {self.max_hours_per_day} | "
                f"OT Rate: {self.overtime_rate}")

class AttendanceManager:
    def __init__(self):
        self.policies = {}

    def add_policy(self, name, max_h, min_h, rate, start, end):
        if name in self.policies:
            raise ValueError(f"Policy {name} already exists.")
        self.policies[name] = AttendancePolicy(name, max_h, min_h, rate, start, end)

    def get_policy(self, name):
        return self.policies.get(name)

    def list_policies(self):
        return list(self.policies.values())

    def check_attendance(self, policy_name, date, check_in_time, worked_hours):
        policy = self.get_policy(policy_name)
        if not policy:
            raise ValueError("Policy not found")

        if not policy.is_work_day(date):
            return "No Work Day (Holiday or Weekend)"
        
        if not policy.is_valid_check_in(check_in_time):
            return f"Invalid Check-in Time: Expected between {policy.work_start} and {policy.work_end}"

        if worked_hours < policy.min_hours_per_day:
            return "Insufficient Hours"
        elif worked_hours > policy.max_hours_per_day:
            overtime = worked_hours - policy.max_hours_per_day
            pay = overtime * policy.overtime_rate
            return f"Overtime: {overtime:.1f} hrs, Extra Pay: ${pay:.2f}"
        else:
            return "Attendance OK"

# Example usage
if __name__ == "__main__":
    mgr = AttendanceManager()
    mgr.add_policy("Standard", 8, 4, 1.5, "09:00", "18:00")

    policy = mgr.get_policy("Standard")
    policy.add_holiday_exception(datetime.date(2025, 5, 1))  # Labor Day

    print("--- Policies ---")
    for p in mgr.list_policies():
        print(p)

    # Simulate attendance check
    result = mgr.check_attendance("Standard", datetime.date(2025, 5, 2),
                                   datetime.time(9, 15), worked_hours=9)
    print("\nAttendance Result:", result)

    result2 = mgr.check_attendance("Standard", datetime.date(2025, 5, 1),
                                    datetime.time(10, 0), worked_hours=6)
    print("Holiday Check Result:", result2)
