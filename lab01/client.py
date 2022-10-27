# -*- coding: utf-8 -*-
import os
import time

data = 'dane.txt'
results = 'wyniki.txt'

time_stamp = 0.0

if (os.path.exists(results)):
    time_stamp = os.stat(results).st_mtime

liczba = input('Podaj liczbe całkowitą: ')
try:
    int(liczba)
except ValueError:
    print(liczba, 'nie jest liczbą całkowitą')
    exit()

with open(data, 'w') as file:
    file.write(liczba)


while (True):
    if not (os.path.exists(results)):
        time.sleep(0.1)
        continue

    if (os.stat(results).st_mtime != time_stamp):
        with open(results, 'r') as f:
            last_line = f.readlines()[-1]
            print(last_line)
            break
