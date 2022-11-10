import sysv_ipc
import os

pid = os.getpid()

klucz = 11
print("Podaj slowo:")
s = input()
mq = sysv_ipc.MessageQueue(klucz)
mq.send(s.encode(), True, pid)

klucz2 = 12
try:
    mq2 = sysv_ipc.MessageQueue(klucz2, sysv_ipc.IPC_CREAT)
    s, t = mq2.receive(True, 0)
    s = s.decode()
    print("Client: odebrałem %s" % s)
except sysv_ipc.ExistentialError:
    print("Serwer zamknął kolejke")
