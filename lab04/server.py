import os
import errno
import time


db = {
    0: "Kowalski",
    1: "Nowak"
}

FIFO = 'kolejka'

# utworzenie kolejki
try:
    os.mkfifo(FIFO)
except OSError as oe: 
    if oe.errno != errno.EEXIST:
        raise

# kolejka otwarta do odczytu 
fifo_in = os.open(FIFO, os.O_RDONLY)

# kolejka otwarta do zapisu,
# Żeby zakończenie klienta jej nie zamykało 
fifo_out1 = os.open(FIFO, os.O_WRONLY|os.O_NDELAY) 

while True:
    r = os.read(fifo_in, 27)
    if len(r)>0:
        req = r.decode()
        req_list = req.split(" ")
        fifo_out2 = os.open(req_list[1], os.O_WRONLY)
        response = "Nie ma"
        if int(req_list[0]) in db:
            response = db[int(req_list[0])]
        os.write(fifo_out2, response.encode())
    else:       
      print("Klient skończył")
      break
    time.sleep(1)