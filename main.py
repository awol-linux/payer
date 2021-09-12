from datetime import datetime, timedelta, date, time
from pydantic import BaseModel
from pydantic.class_validators import validator
from pydantic.fields import T


class Workhours(BaseModel):
    wage: int = 10
    startime: datetime
    endtime: datetime
    day: str

    @validator("endtime", pre=False)
    def parse_endtime(cls, arg):
        return arg + timedelta(hours=12) if arg.hour <= 12 else arg

    @property
    def hours_worked(self):
        delta = self.endtime - self.startime
        return delta.seconds // 3600

    @property
    def pay(self):
        return self.wage * self.hours_worked


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
        while true:
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
                pass
    return days


def output_pretty(days):
    for x in days:
        print(f"On {x.day} you worked {x.hours_worked} and made {x.pay} Dollars")


def main():
    days = calculate()
    output_pretty(days)
    return True


if __name__ == "__main__":
    exit(main())
