import os
from re import A
from time import sleep


while True:
    try:
        with open('buffer', 'r') as buffer:
            line = buffer.readline()
            print(line)

            if not ("/end" in line):
                sleep(0.5)
                continue

            text = buffer.readlines()
            filePath = text[0].strip('\n')

            for text_line in text:
                print(text_line)

            while True:
                with open(filePath, 'w') as a_file:

                    print("\n Write answer: ")
                    answer = input()

                    a_file.write(answer + '\n')
                    if ('\end' in answer):
                        break

            os.remove('buffer')

    except FileNotFoundError as e:
        sleep(0.05)
