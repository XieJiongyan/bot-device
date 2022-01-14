import asyncio
import json
from socket import *

sc = socket(AF_INET, SOCK_STREAM) 

IP = "122.9.138.33"
port = 8100

async def sendLogin():
  loginContent = ["login", "device", "1", "111111"]
  sc.send(bytes(json.dumps(loginContent), encoding= "utf8"))
async def getContent():
  while True:
    re = sc.recv(1000)
    print(re)


def Login():
  sc.connect((IP, port))
  asyncio.run(sendLogin())
  asyncio.run(getContent())

if __name__ == "__main__":
  Login()