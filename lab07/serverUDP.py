# serwer UDP, odbiera napis, odsyła ten napis na wielkich literach
import socket

IP = "127.0.0.1"
port = 5001
bufSize = 1024

# utworzenie gniazda UDP
UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# związanie gniazda z IP i portem
UDPServerSocket.bind((IP, port))

print("serwer UDP działa")

# obsługa nadchodzących datagramów
while (True):
    komB, adres = UDPServerSocket.recvfrom(bufSize)
    print(komB)
    print(adres)
    # wysyłanie odpowiedzi
    kom = komB.decode()
    odpB = kom.upper().encode()
    UDPServerSocket.sendto(odpB, adres)
