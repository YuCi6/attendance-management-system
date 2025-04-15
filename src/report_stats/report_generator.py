import datetime

class ReportGenerator:
    def __init__(self):
        self.attendance_data = []

    def add_record(self, employee_id, date, hours_worked, overtime_hours=0):
        record = {
            "employee_id": employee_id,
            "date": date,
            "hours_worked": hours_worked,
            "overtime_hours": overtime_hours
        }
        self.attendance_data.append(record)

    def generate_daily_report(self, date):
        daily_report = [record for record in self.attendance_data if record["date"] == date]
        return daily_report

    def generate_monthly_report(self, month, year):
        monthly_report = [
            record for record in self.attendance_data if record["date"].month == month and record["date"].year == year
        ]
        return monthly_report

    def generate_yearly_report(self, year):
        yearly_report = [record for record in self.attendance_data if record["date"].year == year]
        return yearly_report

    def generate_overtime_report(self, date_range_start, date_range_end):
        overtime_report = [
            record for record in self.attendance_data if date_range_start <= record["date"] <= date_range_end and record["overtime_hours"] > 0
        ]
        return overtime_report

    def generate_summary(self, report):
        total_hours = sum([record["hours_worked"] for record in report])
        total_overtime = sum([record["overtime_hours"] for record in report])
        return {
            "total_hours": total_hours,
            "total_overtime": total_overtime,
            "average_hours_per_employee": total_hours / len(report) if len(report) > 0 else 0
        }

# Sample usage
if __name__ == "__main__":
    generator = ReportGenerator()
    generator.add_record("001", datetime.date(2025, 4, 1), 8, 2)
    generator.add_record("002", datetime.date(2025, 4, 1), 7, 1.5)
    generator.add_record("001", datetime.date(2025, 4, 2), 8, 3)

    print("--- Daily Report (2025-04-01) ---")
    daily_report = generator.generate_daily_report(datetime.date(2025, 4, 1))
    for record in daily_report:
        print(record)

    print("\n--- Monthly Report (April 2025) ---")
    monthly_report = generator.generate_monthly_report(4, 2025)
    for record in monthly_report:
        print(record)

    print("\n--- Overtime Report ---")
    overtime_report = generator.generate_overtime_report(datetime.date(2025, 4, 1), datetime.date(2025, 4, 30))
    for record in overtime_report:
        print(record)

    print("\n--- Summary ---")
    summary = generator.generate_summary(monthly_report)
    print(summary)
