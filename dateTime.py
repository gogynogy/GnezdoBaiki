from datetime import datetime, timedelta, date
from calendar import monthrange


cur = date.today()
current_datetime = datetime.today()
year = current_datetime.year
month = current_datetime.month
day = current_datetime.day
days = monthrange(year, month)[1]
print(cur + timedelta(days=3))


def GetFinishRentDate(count):
    cur = date.today()
    print(cur + timedelta(days=count))
    return cur + timedelta(days=count)
