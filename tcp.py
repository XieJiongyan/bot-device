import asyncio
import json
from socket import *

sc = socket(AF_INET, SOCK_STREAM) 

IP = "122.9.138.33"
port = 8100
  
async def sendLogin():
  loginContent = {'content': ["login", "device", "1", "111111"]}
  sc.send(bytes(json.dumps(loginContent), encoding= "utf8"))
async def getContent():
  while True:
    try:
      re = sc.recv(1000)
    except BlockingIOError as e:
      # print(e)
      continue
    if re == "" or re == b"":
      break
    print(re)
def read():
  try:
    r = sc.recv(1000)
    print("read from net: ", r)
    return json.loads(r), True
  except BlockingIOError as e:
    return None, False
def write(n: map):
  b = json.dumps(n)
  print(b)
  sc.send(bytes(b, encoding="utf8"))

def Login():
  sc.connect((IP, port))
  
  asyncio.run(sendLogin())
  re = sc.recv(1000)
  sc.setblocking(0)
  print(re)

if __name__ == "__main__":
  Login()
  asyncio.run(getContent())