import os
import time
import errno

import argparse

parser = argparse.ArgumentParser(
    description='Get user input and send to server')
parser.add_argument('--file', type=str, help='Path for server response')

args = parser.parse_args()

if (args.file is None):
    exit("'--file' flag not found")


class FileLockException(Exception):
    pass


# tworzenie pliku zamkowego
while True:
    try:
        # Open file exclusively
        fd = os.open("lockFile", os.O_CREAT | os.O_EXCL | os.O_RDWR)
        break
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
        time.sleep(0.05)
print("plik zamkowy utworzony")

# operacje zabezpieczone plikiem zamkowym
print("operacje zabezpieczone plikiem zamkowym")
# time.sleep(2)
with open('buffer', 'w') as buffer:
    buffer.write('/start\n')
    buffer.write(args.file + "\n")

    buffer.write('text\n')

    buffer.seek(0)
    buffer.write('/end')


# usuwanie pliku zamkowego
os.close(fd)
os.unlink("lockFile")
print("koniec, plik zamkowy zlikwidowany")
