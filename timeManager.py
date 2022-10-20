import schedule
import time
from SQLBD import SQL

BD = SQL()

def job():
    print("jgff")

#schedule.every().day.at("10:30").do(job)
def NulCount():
    schedule.every().monday.at("0:15").do(BD.nullCount())
    schedule.every().minute.at(":17").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)