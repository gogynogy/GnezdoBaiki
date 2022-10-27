from datetime import datetime, timedelta, date
from calendar import monthrange


cur = date.today()
current_datetime = datetime.today()
year = current_datetime.year
month = current_datetime.month
day = current_datetime.day
days = monthrange(year, month)[1]


def GetFinishRentDate(count):
    return str(date.today() + timedelta(days=count))

def GetToodayDate():
    return date.today()