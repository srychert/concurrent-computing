import math
import threading


# check, if `k` is prime
def prime(k):
    s = math.ceil(math.sqrt(k))
    for i in range(2, s+1):
        if k % i == 0:
            return False
    return True


lockPrime = threading.Lock()
primes = []


def primes_from_range(start, end, bar):
    global primes
    slice_total = list(range(start, end))
    slice_primes = []

    for i in slice_total:
        if prime(i):
            slice_primes.append(i)

    with lockPrime:
        primes.extend(slice_primes)

    bar.wait()


start = 2
end = 20
diff = end - start
number_of_threads = 5

take_inputs = True

while take_inputs:
    try:
        start = int(input("Start: "))
        if start < 2:
            raise Exception("Start must be at least 2")

        end = int(input("End: "))
        if end <= start:
            raise Exception("End must be bigger than start")

        number_of_threads = int(input("How many threads: "))
        if number_of_threads < 1:
            raise Exception("At least 1 thread")

        diff = end - start
        if number_of_threads > diff:
            raise Exception(f"No more than {diff}")

        take_inputs = False
    except Exception as e:
        print(str(e))
        continue

b = threading.Barrier(number_of_threads + 1)

segment = math.floor(diff / number_of_threads)
remainer = diff % number_of_threads

print("number_of_threads", number_of_threads,
      "segment", segment, "remainer", remainer)

l = start
r = l + segment
for _ in range(number_of_threads):

    if (remainer > 0):
        r += 1
        remainer -= 1

    t = threading.Thread(target=primes_from_range, args=(l, r, b))
    t.start()

    l = r
    r += segment

# wait for all threads to finish
b.wait()

print(primes)
