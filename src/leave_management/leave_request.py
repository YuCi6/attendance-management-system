# leave_request.py

import datetime

class LeaveRequest:
    def __init__(self, employee_id, leave_type, start_date, end_date, status="Pending"):
        self.employee_id = employee_id
        self.leave_type = leave_type
        self.start_date = start_date
        self.end_date = end_date
        self.status = status

    def approve(self):
        self.status = "Approved"

    def reject(self):
        self.status = "Rejected"

    def __str__(self):
        return f"Leave Request: {self.employee_id} | {self.leave_type} | {self.status} from {self.start_date} to {self.end_date}"

class LeaveManager:
    def __init__(self):
        self.leave_requests = {}

    def request_leave(self, employee_id, leave_type, start_date, end_date):
        leave_id = len(self.leave_requests) + 1
        leave_request = LeaveRequest(employee_id, leave_type, start_date, end_date)
        self.leave_requests[leave_id] = leave_request
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

    def list_leave_requests(self, status=None):
        if status:
            return [request for request in self.leave_requests.values() if request.status == status]
        return list(self.leave_requests.values())

# Sample usage
if __name__ == "__main__":
    manager = LeaveManager()
    leave_id_1 = manager.request_leave("001", "Sick Leave", datetime.date(2025, 4, 10), datetime.date(2025, 4, 12))
    leave_id_2 = manager.request_leave("002", "Vacation", datetime.date(2025, 4, 15), datetime.date(2025, 4, 20))

    print("--- All Leave Requests ---")
    for leave in manager.list_leave_requests():
        print(leave)

    print("\n--- Approving Leave Request ---")
    manager.approve_leave(leave_id_1)
    for leave in manager.list_leave_requests():
        print(leave)

    print("\n--- Pending Leave Requests ---")
    for leave in manager.list_leave_requests("Pending"):
        print(leave)
