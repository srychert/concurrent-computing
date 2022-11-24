import sysv_ipc
from Game import Game
import re


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


def create_mem(key):
    try:
        mem = sysv_ipc.SharedMemory(key)
        return mem
    except sysv_ipc.ExistentialError as e:
        if (str(e) == f"No shared memory exists with the key {key}"):
            return sysv_ipc.SharedMemory(klucz, sysv_ipc.IPC_CREX)
        raise


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


def get_player(player):
    if player == "O":
        return "O"
    else:
        return "X"


def get_next_player(player):
    if player == "O":
        return "X"
    else:
        return "O"


while True:
    print("Waiting for turn")
    sem.acquire()

    odp = czytaj(mem)
    player = get_player(odp[0])
    state = odp[0]

    if state == "W":
        print("You lose")
    elif state == "T":
        print("It is a tie")

    if state == "W" or state == "T":
        sem.remove()
        mem.remove()
        break

    regex = r"((O|X|_)\|(O|X|_)\|(O|X|_)\n){3}"
    search = re.search(regex, odp)

    board = ""
    if search is not None:
        print(odp)
        board = search.group(0)

    game = Game(player, board)
    result = game.make_move()

    if result is not None:
        print(result)
        pisz(mem, result)
        sem.release()
        break

    pisz(mem, get_next_player(player) + "\n" + game.get_board())

    sem.release()
