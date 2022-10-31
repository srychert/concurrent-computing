import os


def silnia(n):
    if n == 0:
        return 1
    # rozgałęziamy proces
    pid = os.fork()
    if pid > 0:  # proces macierzysty
        print("PID stworzonego syna: ", pid)
        # czekanie na zakończenie (jakiegoś) syna
        status = os.wait()
        if os.WIFSIGNALED(status[1]):
            print("ojciec: Sygnał, który zabił proces syna",
                  status[1])
        if os.WIFEXITED(status[1]):
            return n*os.WEXITSTATUS(status[1])
    else:  # syn
        n = n-1
        print("syn: mój PID i n: ", os.getpid(), n)
        wynik = silnia(n)
        print("syn ", os.getpid(), " kończę")
        os._exit(wynik)


print(silnia(5))
