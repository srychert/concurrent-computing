import sysv_ipc
import time

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
    time.sleep(20)
    s, t = mq.receive(True, 0)
    s = s.decode()
    print("Serwer: odebrałem %s  " % s)

    response = "Nie znam takiego słowa"

    if s in slownik:
        response = slownik[s]

    mq2.send(response.encode(), True)


# mq.remove()
