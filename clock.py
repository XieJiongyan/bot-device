import json 
import tcp
import asyncio
from crontab import CronTab
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

clocks = [{}]
aps = BlockingScheduler()
def execAClock(text: str):
  print(text)

def getFromNet(extras: str):
  global clocks, aps
  aps.remove_all_jobs()
  d = json.loads(extras) 
  clocks = d["clocks"]
  for clock in clocks:
    if ~clock['is_active']:
      continue
    aps.add_job(execAClock, CronTrigger.from_crontab(clock['cron']), args=[clock['text']])

async def printFromNet():
  while True:
    re = tcp.read()
    if re == "" or re == b"":
      break
    if re["command"] == "device" and re["options"] == ["total"]:
      getFromNet(re["extras"])
      print(clocks)
if __name__ == "__main__":
  tcp.Login()
  tcp.write({"command":"clock", "options":["get"], "extras": None})
  asyncio.run(printFromNet())