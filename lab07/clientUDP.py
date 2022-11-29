import struct
import socket

serwerAdresPort = ("127.0.0.1", 5001)
bufSize = 1024
UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
score = 0

allowed_moves = ["R", "P", "S", "koniec"]

while True:
    move = input("\nPlay [R,P,S,koniec]: ")
    if move not in allowed_moves:
        print("invalid move")
        continue

    UDPClientSocket.sendto(str.encode(move), serwerAdresPort)

    if move == "koniec":
        break

    print("Waiting for second player move")
    answer = UDPClientSocket.recvfrom(bufSize)
    answer = struct.unpack('!f', answer[0])[0]

    if answer == 403:
        print("2 players already playing")
        break

    if answer == -1:
        print("Second player ended the game")
        print(f"Final score: {score} points")
        break

    print(f"You got {answer} points")
    score += answer
    print(f"You have {score} points in total")
