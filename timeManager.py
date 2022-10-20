import schedule
import time
from SQLBD import SQL
import asyncio

BD = SQL()

async def job():
    print("jgff")

#schedule.every().day.at("10:30").do(job)
# async def NulCount():
#     # schedule.every().monday.at("0:15").do(BD.nullCount())
#     await schedule.every().minute.at(":17").do(job)




async def timer():
    while True:
        schedule.run_pending()
        await time.sleep(1)
        schedule.every().minute.at(":1").do(await job())