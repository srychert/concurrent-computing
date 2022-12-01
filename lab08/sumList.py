import threading
import math

lockSum = threading.Lock()
sum_of_list = 0
list = [i for i in range(1_000_000)]

print("Sum", sum(list))


def sum_list(start, end):
    # print(start, end, list[start:end])
    global sum_of_list
    with lockSum:
        sum_of_list += sum(list[start:end])


def calc():
    number_of_threads = input("How many threads? :")
    global list
    global sum_of_list
    try:
        n = int(number_of_threads)
        if n < 1 or n > len(list):
            raise

        segment = math.floor(len(list) / n)
        remainer = len(list) % n
        is_remainer = True if remainer != 0 else False
        start = 0
        end = segment

        while remainer > 0:
            n -= 1
            end += 1
            remainer -= 1
            t = threading.Thread(target=sum_list, args=(start, end))
            t.start()
            t.join()
            start = end
            end += segment

        if is_remainer:
            start = end - segment
            end = start + segment

        for _ in range(n):
            t = threading.Thread(target=sum_list, args=(start, end))
            t.start()
            t.join()
            start = end
            end = start + segment

        return sum_of_list
    except Exception as e:
        print(str(e))
        print("Wrong number of threads")


calc()
print(sum_of_list)
