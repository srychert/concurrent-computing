# -*- coding: utf-8 -*-
import os
import time

data = 'dane.txt'
results = 'wyniki.txt'


def prosty_wielomian(x):
    return 5 * x**2 + 2*x + 1


def save_to_results(data):
    with open(results, "a") as file:
        file.write(str(data) + "\n")


time_stamp = 0.0
if not (os.path.exists(data)):
    with open(data, 'w') as file:
        file.write('')
        time_stamp = os.stat(data).st_mtime

while (True):
    new_time_stamp = os.stat(data).st_mtime
    if (new_time_stamp != time_stamp):
        with open(data, 'r') as file:
            liczba = int(file.read())
            result = prosty_wielomian(liczba)
            save_to_results(result)
            time_stamp = new_time_stamp
    else:
        time.sleep(1)
