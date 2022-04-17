from email.utils import localtime
import json
from tabnanny import check 
import tcp
import asyncio
from crontab import CronTab
from datetime import datetime
from queue import PriorityQueue
import time

clocks = [{}]

class CronClock:
  priorityQueue = PriorityQueue()

  def putNext(self, ts, content):
    self.priorityQueue.put([ts, content])
  def execContent(self, content):
    print(content['text'])

  # 类似 update, 每 0.5 sec 检查是否有闹钟触发
  def checkThisSec(self):
    print('check')
    ts: float = datetime.now().timestamp()
    # print("size:", self.priorityQueue.qsize)
    while not self.priorityQueue.empty():
      # print(self.priorityQueue.qsize)
      nextAlarm = self.priorityQueue.get()
      # print("nextAlarm: ", nextAlarm, "ts:", ts)
      if nextAlarm[0] <= ts:
        self.execContent(nextAlarm[1])
        self.add(nextAlarm[1])
      else:
        self.priorityQueue.put(nextAlarm)
        break 

  async def start(self):
    print("start")
    while True:
      self.checkThisSec()
      await asyncio.sleep(0.5)

  def add(self, alarm: dict):
    entry = CronTab(alarm['cron'])
    ts: float = datetime.now().timestamp() + entry.next()
    print("add ts: ", ts, datetime.fromtimestamp(ts))
    self.putNext(ts, alarm)
  
  def clear(self):
    while not self.priorityQueue.empty():
      self.priorityQueue.get()

def exec():
  print(1)

global cronClock
cronClock = CronClock()

def getFromNet(extras: str):
  global clocks, aps
  d = json.loads(extras) 
  clocks = d["clocks"]
  # print('d::: ' + str(clocks))

  cronClock.clear()
  for clock in clocks:
    if not clock['is_active']:
      continue
    cronClock.add(clock)
  
async def main():
  cronClock.start()
  asyncio.create_task(cronClock.start())
  while True:
    re, success = tcp.read()
    if not success:
      await asyncio.sleep(0.1)
      continue
    if re == "" or re == b"":
      break
    if re["command"] == "device" and re["options"] == ["total"]:
      getFromNet(re["extras"])
      # print(clocks)


loop = asyncio.get_event_loop()

if __name__ == "__main__":
  tcp.Login()
  tcp.write({"command":"clock", "options":["get"], "extras": None})

  loop.run_until_complete(main())
  loop.close()
