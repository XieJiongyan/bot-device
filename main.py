import tcp 
import clock 
import asyncio 

async def main():
  asyncio.create_task(clock.cronClock.start())
  while True:
    re, success = tcp.read()
    if not success:
      await asyncio.sleep(0.1)
      continue
    if re == "" or re == b"":
      break
    if re["command"] == "device" and re["options"] == ["total"]:
      clock.getFromNet(re["extras"])
      # print(clocks)


loop = asyncio.get_event_loop()

if __name__ == "__main__":
  tcp.Login()
  tcp.write({"command":"clock", "options":["get"], "extras": None})

  loop.run_until_complete(main())
  loop.close()
