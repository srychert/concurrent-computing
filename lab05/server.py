import sysv_ipc
import time
import signal
import sys
import os

print("Pid programu:", os.getpid())

slownik = {
    "pies": "dog",
    "kot": "cat"
}

klucz = 11
klucz2 = 12

mq = sysv_ipc.MessageQueue(klucz, sysv_ipc.IPC_CREAT)
mq2 = sysv_ipc.MessageQueue(klucz2, sysv_ipc.IPC_CREAT)
print("kolejka utworzona")


def handler(signum, frame):
    print("Obsługa sygnału", signum)


def handler1(signum, frame):
    print("Inna obsługa sygnału", signum)
    mq.remove()
    mq2.remove()
    print("Kończę program")
    sys.exit(0)


# przypisanie obsługi sygnału do SIGINT
signal.signal(signal.SIGHUP, handler)
signal.signal(signal.SIGTERM, handler)


# przypisanie obsługi sygnału do SIGUSR1
signal.signal(signal.SIGUSR1, handler1)

while True:
    msg = ""
    try:
        s, t = mq.receive(True, 0)
        msg = s.decode()
        print("Serwer: odebrałem %s " % msg)
    except sysv_ipc.Error as e:
        print(str(e))
        continue

    response = "Nie znam takiego słowa"

    if msg in slownik:
        response = slownik[msg]

    mq2.send(response.encode(), True)
    print("wysłane")
    time.sleep(10)
    print("po")
