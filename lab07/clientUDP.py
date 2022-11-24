# klient UDP, dwukrotmie  wysyła napis i odbiera napis

import socket

komA = "aaaaa"
komAB = str.encode(komA)
serwerAdresPort = ("127.0.0.1", 5001)
klientAdresPort = ("127.0.0.1", 5002)
bufSize = 1024
# tworzy gniazdo UDP po stronie klienta
UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# związuje gniazdo z parą adres, port - można pominąć
# UDPClientSocket.bind(klientAdresPort)

# wysyła do serwera przez utworzone gniazdo
UDPClientSocket.sendto(komAB, serwerAdresPort)
odp = UDPClientSocket.recvfrom(bufSize)
print(odp)
UDPClientSocket.sendto("bbb".encode(), serwerAdresPort)
odp = UDPClientSocket.recvfrom(bufSize)
print(odp)
