from datetime import datetime, timedelta, time
from typing import List, Dict


class AttendanceRule:
    def __init__(self, start_time: time, end_time: time, grace_period: int = 5, allow_flex: bool = False):
        self.start_time = start_time
        self.end_time = end_time
        self.grace_period = grace_period  # minutes allowed to be late without penalty
        self.allow_flex = allow_flex  # whether flexible hours are allowed

    def is_late(self, check_in_time: time) -> bool:
        threshold = (datetime.combine(datetime.today(), self.start_time) + timedelta(minutes=self.grace_period)).time()
        return check_in_time > threshold

    def is_early_leave(self, check_out_time: time) -> bool:
        return check_out_time < self.end_time

    def __str__(self):
        return (f"Start: {self.start_time}, End: {self.end_time}, "
                f"Grace: {self.grace_period} min, Flex: {self.allow_flex}")


class LeavePolicy:
    def __init__(self):
        self.annual_days = 10
        self.sick_days = 5
        self.unpaid_days = 0
        self.holidays: List[str] = []  # Format: ['2025-01-01', '2025-02-11']

    def is_holiday(self, date_str: str) -> bool:
        return date_str in self.holidays

    def add_holiday(self, date_str: str):
        if date_str not in self.holidays:
            self.holidays.append(date_str)

    def remove_holiday(self, date_str: str):
        if date_str in self.holidays:
            self.holidays.remove(date_str)


class OvertimePolicy:
    def __init__(self):
        self.enabled = True
        self.minimum_duration = 1  # in hours
        self.approval_required = True
        self.multiplier = 1.5  # salary multiplier for overtime hours

    def calculate_pay(self, base_hourly: float, hours: float) -> float:
        if hours < self.minimum_duration:
            return 0.0
        return base_hourly * hours * self.multiplier


class AttendancePolicyManager:
    def __init__(self):
        self.rules_by_role: Dict[str, AttendanceRule] = {}
        self.leave_policy = LeavePolicy()
        self.overtime_policy = OvertimePolicy()
        self.blacklisted_locations: List[str] = []

    def set_rule_for_role(self, role: str, rule: AttendanceRule):
        self.rules_by_role[role] = rule

    def get_rule_for_role(self, role: str) -> AttendanceRule:
        return self.rules_by_role.get(role)

    def is_location_allowed(self, location: str) -> bool:
        return location not in self.blacklisted_locations

    def add_blacklisted_location(self, location: str):
        if location not in self.blacklisted_locations:
            self.blacklisted_locations.append(location)

    def remove_blacklisted_location(self, location: str):
        if location in self.blacklisted_locations:
            self.blacklisted_locations.remove(location)

    def print_all_policies(self):
        print("考勤规则列表：")
        for role, rule in self.rules_by_role.items():
            print(f"  [{role}]: {rule}")

        print("\n节假日安排：", self.leave_policy.holidays)
        print("是否启用加班制度：", self.overtime_policy.enabled)


# 示例代码（可注释掉以用于导入模块）
if __name__ == "__main__":
    manager = AttendancePolicyManager()

    # 设置规则
    dev_rule = AttendanceRule(start_time=time(9, 0), end_time=time(18, 0), grace_period=10, allow_flex=True)
    hr_rule = AttendanceRule(start_time=time(8, 30), end_time=time(17, 30), grace_period=5, allow_flex=False)

    manager.set_rule_for_role("Developer", dev_rule)
    manager.set_rule_for_role("HR", hr_rule)

    # 添加假期
    manager.leave_policy.add_holiday("2025-01-01")
    manager.leave_policy.add_holiday("2025-05-01")

    # 黑名单位置
    manager.add_blacklisted_location("Overseas VPN")
    manager.add_blacklisted_location("Home Office")

    # 测试加班工资
    print("\n加班工资（基础时薪30，时长2小时）：", manager.overtime_policy.calculate_pay(30.0, 2))

    # 打印所有政策
    manager.print_all_policies()
