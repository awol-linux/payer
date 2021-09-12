from datetime import datetime, timedelta, date, time
from pydantic import BaseModel
from pydantic.class_validators import validator
from pydantic.error_wrappers import ValidationError
from textwrap import dedent


class Workhours(BaseModel):
    wage: int = 14
    startime: datetime
    endtime: datetime
    day: str
    overtime_limit: int = 8

    @validator("endtime", pre=False)
    def parse_endtime(cls, arg):
        return arg + timedelta(hours=12) if arg.hour <= 12 else arg

    @property
    def hours_worked(self):
        delta = self.endtime - self.startime
        return delta.seconds // 3600

    @property
    def seconds_worked(self):
        delta = self.endtime - self.startime
        return delta.seconds

    @property
    def pay(self):
        second_wage = float(self.wage) / float(3600)
        if self.seconds_worked > (self.overtime_limit * 3600):
            normal_pay = self.overtime_limit * self.wage
            overtime = (self.seconds_worked - (self.overtime_limit * 3600)) * (
                second_wage * 1.5
            )
            return round(normal_pay + overtime, 2)
        return round((second_wage * self.seconds_worked), 2)


def calculate():
    days = []
    for count, day in enumerate(["mon", "tue", "wed", "thur", "fri"]):
        today = date.today()
        last_week = today - timedelta(days=7)
        attempt = last_week
        for _ in range(7):
            if attempt.weekday() == 6:
                break
            attempt = last_week - timedelta(days=1)
        date_obj = last_week + timedelta(days=count)
        while True:
            did_work = input(f"Did you work on {day}: ").lower()
            if did_work in ("n", "no"):
                break
            if not did_work in ("y", "yes"):
                continue
            start, end = input(f"{day} start: "), input(f"{day} end: ")
            try:
                if start != "" and end != "":
                    days.append(
                        Workhours(
                            startime=f"{date_obj}T{start}",
                            endtime=f"{date_obj}T{end}",
                            day=day.capitalize(),
                        )
                    )
                break
            except ValidationError:
                print("Please add valid Time")
    return days


def output_pretty(days):
    for x in days:
        print(
            dedent(
                f"""
        On {x.day} 
        you started at {x.startime.strftime("%I:%M %p")}
        Worked until {x.endtime.strftime("%I:%M %p")}
        Which totaled {x.hours_worked} hours and {int((x.seconds_worked % 3600) / 60)} minutes
        And made {x.pay} Dollars"""
            )
        )


def main():
    days = calculate()
    output_pretty(days)
    return True


if __name__ == "__main__":
    exit(main())
