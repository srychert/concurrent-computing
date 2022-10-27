# -*- coding: utf-8 -*-
import os
import time
import errno
import argparse

parser = argparse.ArgumentParser(
    description='Specify path for client data')
parser.add_argument('--file', type=str, help='Path for data file')

args = parser.parse_args()

if (args.file is None):
    exit("'--file' flag not found")


# tworzenie pliku zamkowego
while True:
    try:
        # Open file exclusively
        fd = os.open("lockFile", os.O_CREAT | os.O_EXCL | os.O_RDWR)
        break
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
        print("Serwer zajęty, proszę czekać")
        time.sleep(3)

print("Plik zamkowy utworzony")

# operacje zabezpieczone plikiem zamkowym
with open('buffer', 'w') as buffer:
    buffer.write(args.file+"\n")

    print("Napisz '/end' aby zakończyć")
    while True:
        print("Podaj pytanie: ")
        question = input()

        if ("/end" in question):
            break

        buffer.write(question + "\n")

    buffer.write('/end')


# zamknięcie pliku zamkowego
os.close(fd)
