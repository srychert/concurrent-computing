import os
import time
import errno
import re


stamp = time.time() * 1000000

FIFO = "kolejka"
FIFO2 = "kolejka%d" % (stamp)

print(FIFO2)

# int w formacie 001
slowo = input()

matched = re.search("^[0-9][0-9][0-9]", slowo)
if matched is None:
    exit()

id = matched.group(0)

fifo_out = os.open(FIFO, os.O_WRONLY)
os.write(fifo_out, f"{id} {FIFO2}".encode())

# utworzenie kolejki
try:
    os.mkfifo(FIFO2)
except OSError as oe:
    if oe.errno != errno.EEXIST:
        raise

fifo_in = os.open(FIFO2, os.O_RDONLY)
while True:
    r = os.read(fifo_in, 24) # czytanie 2 bajtów
    if len(r)>0:
      print("Serwer: %s" % r.decode())
      break
    time.sleep(1) # spowolnienie do testowania

os.remove(FIFO2)