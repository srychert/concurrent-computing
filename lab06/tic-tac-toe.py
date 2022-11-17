import sysv_ipc
import time


klucz = 31
NULL_CHAR = '\0'


def create_sem(key, init_value):
    try:
        sem = sysv_ipc.Semaphore(key)
        return sem
    except sysv_ipc.ExistentialError as e:
        if (str(e) == "No semaphore exists with the specified key"):
            return sysv_ipc.Semaphore(key, sysv_ipc.IPC_CREX, 0o700, init_value)
        raise


def remove_sem(sem):
    sem.remove()


def create_mem(key):
    try:
        mem = sysv_ipc.SharedMemory(key)
        return mem
    except sysv_ipc.ExistentialError as e:
        if (str(e) == f"No shared memory exists with the key {key}"):
            return sysv_ipc.SharedMemory(klucz, sysv_ipc.IPC_CREX)
        raise


def remove_mem(mem):
    mem.remove()


sem = create_sem(klucz, 1)
mem = create_mem(klucz)
# sem.remove()
# mem.remove()


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


def next_player(player):
    text = " to play\n"
    next_player = ""
    if player == "X" or player == " ":
        next_player = "O"
    elif player == "O":
        next_player = "X"
    else:
        raise Exception(f"Wrong player type: {player}")

    return next_player + text


# Game here
board = "_|_|_\n"*3
sem.acquire()
# time.sleep(3)
odp = czytaj(mem)
next = next_player(odp[0])
pisz(mem, next + board)
print(czytaj(mem))
sem.release()
