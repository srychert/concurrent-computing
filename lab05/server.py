import sysv_ipc
import time
import signal
import sys
import os

print(os.getpid())


def handler(signum, frame):
    print('Obsługa sygnału ', signum)


def handler1(signum, frame):
    print(' Inna obsługa sygnału ', signum)
    sys.exit(0)


# przypisanie obsługi sygnału do SIGINT
signal.signal(signal.SIGHUP, handler)
signal.signal(signal.SIGTERM, handler)


# przypisanie obsługi sygnału do SIGUSR1
signal.signal(signal.SIGUSR1, handler1)

slownik = {
    "pies": "dog",
    "kot": "cat"
}

klucz = 11
klucz2 = 12

mq = sysv_ipc.MessageQueue(klucz, sysv_ipc.IPC_CREAT)
mq2 = sysv_ipc.MessageQueue(klucz2, sysv_ipc.IPC_CREAT)

# mq.remove()
# mq2.remove()

print("kolejka utworzona")

while True:
    s, t = mq.receive(True, 0)
    s = s.decode()
    print("Serwer: odebrałem %s  " % s)

    response = "Nie znam takiego słowa"

    if s in slownik:
        response = slownik[s]

    mq2.send(response.encode(), True)
    print("wysłane")
    time.sleep(10)
    print("po")
