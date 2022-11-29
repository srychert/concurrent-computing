import socket
import struct
import pprint

IP = "127.0.0.1"
port = 5001
bufSize = 1024

# utworzenie gniazda UDP
UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# związanie gniazda z IP i portem
UDPServerSocket.bind((IP, port))

print("serwer UDP działa")


def rock_paper_scissors(moves):
    p1, p2 = moves

    results = {
        "PP": (0.5, 0.5), "PR": (1, 0), "PS": (0, 1),
        "RP": (0, 1), "RR": (0.5, 0.5), "RS": (1, 0),
        "SP": (1, 0), "SR": (0, 1), "SS": (0.5, 0.5)
    }

    i = p1[1] + p2[1]
    r = results[i]

    return [(p1[0], r[0]), (p2[0], r[1])]


scores = {}

while (True):
    move, adres = UDPServerSocket.recvfrom(bufSize)
    move = move.decode()

    if move == "koniec":
        print("ending game\n")
        for k in scores.keys():
            if k != adres:
                UDPServerSocket.sendto(struct.pack('!f', -1), k)
        scores = {}
        continue

    if adres not in scores:
        if len(scores) < 2:
            print("new player!")
            scores.update({adres: {"score": 0, "move": None}})
        else:
            UDPServerSocket.sendto(struct.pack('!f', 403), adres)
            continue

    scores[adres]["move"] = move

    moves = []
    for k, v in scores.items():
        if v["move"] is not None:
            moves.append((k, v["move"]))

    if len(moves) != 2:
        continue

    result = rock_paper_scissors(moves)

    print("Scores:")
    for r in result:
        scores[r[0]]["score"] += r[1]
        print(r[0], scores[r[0]])
        scores[r[0]]["move"] = None
        UDPServerSocket.sendto(struct.pack('!f', r[1]), r[0])

    # pprint.pprint(scores)
