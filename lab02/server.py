# -*- coding: utf-8 -*-
import os
from time import sleep

# create buffer if not exists
try:
    f = open("buffer", "x")
    f.close()
except:
    pass

print("Serwer działa")
while True:
    with open('buffer', 'r+') as buffer:
        # check if there is answer file path in buffer
        line = buffer.readline()
        if len(line.strip()) == 0:
            sleep(0.5)
            continue

        # print questions
        lines = buffer.readlines()
        for l in lines:
            print(l.strip())

        # clear buffer after reading
        buffer.seek(0)
        buffer.truncate()

        # create answer file
        a_file = open(line.strip(), "w")
        print("Napisz '/end' aby zakończyć")
        while True:
            print("Wpisz odpowiedź: ")
            answer = input()
            a_file.write(answer + "\n")

            if ("/end" in answer):
                break

        # close file and remove lockFile
        a_file.close()
        os.unlink("lockFile")
        print("koniec, plik zamkowy zlikwidowany")
