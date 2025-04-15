import datetime

class LeaveRequest:
    def __init__(self, employee_id, leave_type, start_date, end_date, status="Pending"):
        self.employee_id = employee_id
        self.leave_type = leave_type
        self.start_date = start_date
        self.end_date = end_date
        self.status = status
        self.request_date = datetime.date.today()

    def approve(self):
        self.status = "Approved"
        print(f"[{datetime.datetime.now()}] Leave approved for employee {self.employee_id}.")

    def reject(self):
        self.status = "Rejected"
        print(f"[{datetime.datetime.now()}] Leave rejected for employee {self.employee_id}.")

    def cancel(self):
        if self.status == "Pending":
            self.status = "Cancelled"
            print(f"[{datetime.datetime.now()}] Leave request cancelled by employee {self.employee_id}.")
        else:
            print(f"[{datetime.datetime.now()}] Cannot cancel. Leave already {self.status}.")

    def leave_duration(self):
        return (self.end_date - self.start_date).days + 1

    def __str__(self):
        return (f"Leave Request: {self.employee_id} | {self.leave_type} | {self.status} "
                f"| From {self.start_date} To {self.end_date} | {self.leave_duration()} days")


class LeaveManager:
    def __init__(self):
        self.leave_requests = {}
        self.employee_registry = {}

    def register_employee(self, employee_id, name, department):
        self.employee_registry[employee_id] = {
            "name": name,
            "department": department
        }
        print(f"Employee registered: {employee_id} - {name} ({department})")

    def request_leave(self, employee_id, leave_type, start_date, end_date):
        if employee_id not in self.employee_registry:
            raise ValueError(f"Employee ID {employee_id} not registered.")
        if start_date > end_date:
            raise ValueError("Start date must not be after end date.")

        leave_id = len(self.leave_requests) + 1
        leave_request = LeaveRequest(employee_id, leave_type, start_date, end_date)
        self.leave_requests[leave_id] = leave_request
        print(f"Leave requested (ID {leave_id}) by {employee_id}: {leave_type} from {start_date} to {end_date}")
        return leave_id

    def approve_leave(self, leave_id):
        if leave_id in self.leave_requests:
            self.leave_requests[leave_id].approve()
        else:
            raise KeyError(f"Leave request {leave_id} not found.")

    def reject_leave(self, leave_id):
        if leave_id in self.leave_requests:
            self.leave_requests[leave_id].reject()
        else:
            raise KeyError(f"Leave request {leave_id} not found.")

    def cancel_leave(self, leave_id):
        if leave_id in self.leave_requests:
            self.leave_requests[leave_id].cancel()
        else:
            raise KeyError(f"Leave request {leave_id} not found.")

    def list_leave_requests(self, status=None, employee_id=None):
        result = list(self.leave_requests.items())
        if status:
            result = [item for item in result if item[1].status == status]
        if employee_id:
            result = [item for item in result if item[1].employee_id == employee_id]
        return result

    def print_leave_summary(self):
        print("\n===== Leave Summary =====")
        for leave_id, leave in self.leave_requests.items():
            emp = self.employee_registry.get(leave.employee_id, {})
            print(f"ID: {leave_id} | {emp.get('name', leave.employee_id)} | {leave}")

    def list_employee_leaves(self, employee_id):
        leaves = self.list_leave_requests(employee_id=employee_id)
        print(f"\n--- Leave History for {employee_id} ---")
        for leave_id, leave in leaves:
            print(f"Leave ID: {leave_id} | {leave}")


# Sample usage
if __name__ == "__main__":
    manager = LeaveManager()

    # Register employees
    manager.register_employee("001", "Alice", "HR")
    manager.register_employee("002", "Bob", "IT")

    # Create leave requests
    leave_id_1 = manager.request_leave("001", "Sick Leave", datetime.date(2025, 4, 10), datetime.date(2025, 4, 12))
    leave_id_2 = manager.request_leave("002", "Vacation", datetime.date(2025, 4, 15), datetime.date(2025, 4, 20))
    leave_id_3 = manager.request_leave("001", "Personal", datetime.date(2025, 5, 1), datetime.date(2025, 5, 3))

    # List all requests
    manager.print_leave_summary()

    # Approve one and reject another
    manager.approve_leave(leave_id_1)
    manager.reject_leave(leave_id_2)

    # Cancel a pending request
    manager.cancel_leave(leave_id_3)

    # List pending only
    print("\n--- Pending Leave Requests ---")
    for lid, leave in manager.list_leave_requests(status="Pending"):
        print(f"Leave ID: {lid} | {leave}")

    # View leave history of a specific employee
    manager.list_employee_leaves("001")
