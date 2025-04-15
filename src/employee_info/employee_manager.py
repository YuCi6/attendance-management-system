# employee_manager.py

class Employee:
    def __init__(self, emp_id, name, department, position):
        self.emp_id = emp_id
        self.name = name
        self.department = department
        self.position = position
        self.status = 'active'

    def update_info(self, name=None, department=None, position=None):
        if name:
            self.name = name
        if department:
            self.department = department
        if position:
            self.position = position

    def deactivate(self):
        self.status = 'inactive'

    def __str__(self):
        return f"{self.emp_id} - {self.name}, {self.position} in {self.department} ({self.status})"


class EmployeeManager:
    def __init__(self):
        self.employees = {}

    def add_employee(self, emp_id, name, department, position):
        if emp_id in self.employees:
            raise ValueError("Employee ID already exists.")
        self.employees[emp_id] = Employee(emp_id, name, department, position)

    def remove_employee(self, emp_id):
        if emp_id in self.employees:
            del self.employees[emp_id]
        else:
            raise KeyError("Employee not found.")

    def get_employee(self, emp_id):
        return self.employees.get(emp_id)

    def update_employee(self, emp_id, name=None, department=None, position=None):
        employee = self.get_employee(emp_id)
        if employee:
            employee.update_info(name, department, position)
        else:
            raise KeyError("Employee not found.")

    def list_active_employees(self):
        return [emp for emp in self.employees.values() if emp.status == 'active']

    def list_all_employees(self):
        return list(self.employees.values())

    def deactivate_employee(self, emp_id):
        emp = self.get_employee(emp_id)
        if emp:
            emp.deactivate()
        else:
            raise KeyError("Employee not found.")

    def search_employees_by_name(self, keyword):
        return [emp for emp in self.employees.values() if keyword.lower() in emp.name.lower()]

    def search_by_department(self, department):
        return [emp for emp in self.employees.values() if emp.department == department]

    def generate_employee_summary(self):
        total = len(self.employees)
        active = len(self.list_active_employees())
        inactive = total - active
        summary = (
            f"Total Employees: {total}\n"
            f"Active: {active}\n"
            f"Inactive: {inactive}\n"
        )
        return summary

    def export_to_dict(self):
        return {
            emp_id: {
                "name": emp.name,
                "department": emp.department,
                "position": emp.position,
                "status": emp.status,
            }
            for emp_id, emp in self.employees.items()
        }

    def import_from_dict(self, data):
        for emp_id, info in data.items():
            emp = Employee(emp_id, info['name'], info['department'], info['position'])
            emp.status = info.get('status', 'active')
            self.employees[emp_id] = emp

# Sample usage
if __name__ == "__main__":
    manager = EmployeeManager()
    manager.add_employee("001", "Alice", "HR", "Manager")
    manager.add_employee("002", "Bob", "IT", "Developer")
    manager.deactivate_employee("001")

    print("--- All Employees ---")
    for emp in manager.list_all_employees():
        print(emp)

    print("\n--- Active Employees ---")
    for emp in manager.list_active_employees():
        print(emp)

    print("\n--- Summary ---")
    print(manager.generate_employee_summary())
