import datetime
from typing import List, Dict, Optional, Tuple


class AttendanceRecord:
    def __init__(self, employee_id: str, date: datetime.date, hours_worked: float, overtime_hours: float = 0.0):
        self.employee_id = employee_id
        self.date = date
        self.hours_worked = hours_worked
        self.overtime_hours = overtime_hours

    def to_dict(self) -> Dict[str, any]:
        return {
            "employee_id": self.employee_id,
            "date": self.date,
            "hours_worked": self.hours_worked,
            "overtime_hours": self.overtime_hours
        }

    def __repr__(self):
        return f"<AttendanceRecord {self.employee_id} on {self.date}>"


class Report:
    def __init__(self, records: List[AttendanceRecord]):
        self.records = records

    def total_hours(self) -> float:
        return sum(record.hours_worked for record in self.records)

    def total_overtime(self) -> float:
        return sum(record.overtime_hours for record in self.records)

    def average_hours_per_employee(self) -> float:
        unique_employees = {record.employee_id for record in self.records}
        return self.total_hours() / len(unique_employees) if unique_employees else 0

    def summary(self) -> Dict[str, float]:
        return {
            "total_hours": self.total_hours(),
            "total_overtime": self.total_overtime(),
            "average_hours_per_employee": self.average_hours_per_employee()
        }

    def __repr__(self):
        return f"<Report with {len(self.records)} records>"


class ReportGenerator:
    def __init__(self):
        self._attendance_data: List[AttendanceRecord] = []

    def add_record(self, employee_id: str, date: datetime.date, hours_worked: float, overtime_hours: float = 0.0) -> None:
        record = AttendanceRecord(employee_id, date, hours_worked, overtime_hours)
        self._attendance_data.append(record)

    @property
    def records(self) -> List[AttendanceRecord]:
        return self._attendance_data

    def _filter_by_date_range(self, start: datetime.date, end: datetime.date) -> List[AttendanceRecord]:
        return [record for record in self._attendance_data if start <= record.date <= end]

    def _filter_by_exact_date(self, date: datetime.date) -> List[AttendanceRecord]:
        return [record for record in self._attendance_data if record.date == date]

    def _filter_by_month_year(self, month: int, year: int) -> List[AttendanceRecord]:
        return [record for record in self._attendance_data if record.date.month == month and record.date.year == year]

    def _filter_by_year(self, year: int) -> List[AttendanceRecord]:
        return [record for record in self._attendance_data if record.date.year == year]

    def _filter_overtime(self, records: List[AttendanceRecord]) -> List[AttendanceRecord]:
        return [record for record in records if record.overtime_hours > 0]

    def generate_daily_report(self, date: datetime.date) -> Report:
        return Report(self._filter_by_exact_date(date))

    def generate_monthly_report(self, month: int, year: int) -> Report:
        return Report(self._filter_by_month_year(month, year))

    def generate_yearly_report(self, year: int) -> Report:
        return Report(self._filter_by_year(year))

    def generate_overtime_report(self, start_date: datetime.date, end_date: datetime.date) -> Report:
        all_in_range = self._filter_by_date_range(start_date, end_date)
        overtime_records = self._filter_overtime(all_in_range)
        return Report(overtime_records)


# Optional: Utility functions for output
def print_report(title: str, report: Report) -> None:
    print(f"\n--- {title} ---")
    for record in report.records:
        print(record.to_dict())


def print_summary(report: Report) -> None:
    print("\n--- Summary ---")
    for key, value in report.summary().items():
        print(f"{key}: {value:.2f}")


# Example Usage
def main():
    generator = ReportGenerator()

    # Sample data
    generator.add_record("001", datetime.date(2025, 4, 1), 8, 2)
    generator.add_record("002", datetime.date(2025, 4, 1), 7, 1.5)
    generator.add_record("001", datetime.date(2025, 4, 2), 8, 3)
    generator.add_record("003", datetime.date(2025, 4, 3), 6, 0)
    generator.add_record("002", datetime.date(2025, 4, 5), 7.5, 2)

    # Reports
    daily_report = generator.generate_daily_report(datetime.date(2025, 4, 1))
    print_report("Daily Report (2025-04-01)", daily_report)

    monthly_report = generator.generate_monthly_report(4, 2025)
    print_report("Monthly Report (April 2025)", monthly_report)

    yearly_report = generator.generate_yearly_report(2025)
    print_report("Yearly Report (2025)", yearly_report)

    overtime_report = generator.generate_overtime_report(datetime.date(2025, 4, 1), datetime.date(2025, 4, 30))
    print_report("Overtime Report (April 2025)", overtime_report)

    print_summary(monthly_report)
