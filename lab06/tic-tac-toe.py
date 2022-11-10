import sysv_ipc
klucz = 31
NULL_CHAR = '\0'


def create(klucz: int):
    sem1 = sysv_ipc.Semaphore(klucz, sysv_ipc.IPC_CREX, 0o700, 0)
    sem2 = sysv_ipc.Semaphore(klucz+1, sysv_ipc.IPC_CREX, 0o700, 1)
    mem = sysv_ipc.SharedMemory(klucz, sysv_ipc.IPC_CREX)
    return sem1, sem2, mem


def remove(mem_id, sem1_id, sem2_id):
    sysv_ipc.remove_shared_memory(mem_id)
    sysv_ipc.remove_semaphore(sem1_id)
    sysv_ipc.remove_semaphore(sem2_id)


sem1, sem2, mem = create(klucz)


def pisz(mem, s):
    s += NULL_CHAR
    s = s.encode()
    mem.write(s)


def czytaj(mem):
    s = mem.read()
    s = s.decode()
    i = s.find(NULL_CHAR)
    if i != -1:
        s = s[:i]
    return s


s = "test"
pisz(mem, s)
for i in range(0, 1):
    print(s)
    sem1.acquire(timeout=5)
    s = czytaj(mem)
    s = s+'a'
    pisz(mem, s)
    sem2.release()


print(s)
remove(mem.id, sem1.id, sem2.id)
