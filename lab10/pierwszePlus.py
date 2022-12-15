import time
import math
from multiprocessing import Process, Lock, Queue
from multiprocessing.sharedctypes import Value, Array

l=1000000
r=2000000

def pierwsza(k):
    # sprawdzenie, czy k jest pierwsza
    for i in range (2, k - 1):
        if i * i > k:
            return True
        if k % i == 0:
            return False
    return True


def pierwsza1(k, mlp):
    # sprawdzenie, czy k jest pierwsza
    # korzystając z zestawu małych liczb pierwszych mlp
    for p in mlp:
        if k%p == 0:
            return False
        if p*p>k:
            return True
    return True

p_list = []

def add_to_queue_if_prime(l, mlp, q):
    for k in l:
        if(pierwsza1(k, mlp)):
            q.put(k)

def licz(l, r, q):
    # tworzenie listy małych liczb pierwszych
    mlp = []
    s = math.ceil(math.sqrt(r))
    for i in range (2, s + 1):
        if pierwsza(i):
            mlp.append(i)

    # hard coded step for 10 process in range l r specified above
    for i in range (l,r+1, 1_000_00):
        p = Process(target=add_to_queue_if_prime, args=(range(i, i+1000), mlp, q))
        p.start()
        p_list.append(p)




if __name__ == '__main__':
    q = Queue()

    print(l, r)
    start = time.time()
    licz(l, r, q)
    for p in p_list:
        p.join()
    print( time.time()-start)
    # primes = []
    while True:
        if q.empty():
            break
        prime_num = q.get()
        # primes.append(prime_num)
