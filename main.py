import tcp 
import clock 
import asyncio 

async def listen():
  while True:
    re = tcp.read()
    if re == "" or re == b"":
      break
    if re["command"] == "device" and re["options"] == ["total"]:
      clock.getFromNet(re["extras"])
      print(clock.clocks)
      
if __name__ == "__main__":
  tcp.Login()
  tcp.write({"command":"clock", "options":["get"], "extras": None})
  asyncio.run(listen())