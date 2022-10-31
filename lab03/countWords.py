# -*- coding: utf-8 -*-
import argparse
import os

parser = argparse.ArgumentParser(
    description='Fork searching')
parser.add_argument('--p', type=str, help='File path to begin search')
parser.add_argument('--s', type=str, help='Word to search for')

args = parser.parse_args()

if (args.p is None):
    exit("'--p' flag not found")

if (args.s is None):
    exit("'--s' flag not found")


def readFile(path):
    with open(path, "r") as file:
        lines = file.readlines()
        files = []
        count = 0

        for line in lines:
            if "\input" in line:
                start = line.find("{")+1
                end = line.find("}")

                files.append(line[start:end])
            else:
                count += line.count(args.s)

    return {"files": files, "count": count}


def work(files, count):
    fileToRead = files.pop()
    result = readFile(fileToRead)
    print("Znalazłem %d wystapienie słowa %s w pliku %s" %
          (result["count"], args.s, fileToRead))

    files += result["files"]
    count += result["count"]

    if len(files) == 0:
        return count

    pid = os.fork()

    # proces macierzysty
    if pid > 0:
        # czekamy na wynik od jakiegoś syna
        status = os.wait()
        if os.WIFEXITED(status[1]):
            return os.WEXITSTATUS(status[1])
    # syn
    else:
        count2 = work(files, count)
        os._exit(count2)


word_count = work([args.p], 0)
print(word_count)
