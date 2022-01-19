import json 
import tcp
import asyncio

clocks = [{}]

def getFromNet(extras: str):
  global clocks
  d = json.loads(extras) 
  clocks = d["clocks"]

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