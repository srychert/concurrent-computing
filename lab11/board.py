import PySimpleGUI as sg
from colors import get_random_colors
import struct
import socket
import time
import json

sg.theme('Dark Blue 3')

layout = [[sg.Text('Choose your game port', key='-TITLE-')],
          [sg.Input(default_text="5001", key="-INPUT-")],
          [sg.Text('', key='-ERROR-')],
          [sg.Button('OK'), sg.Exit()]]

window = sg.Window('Game setup', layout)

IP = "127.0.0.1"
bufSize = 1024
UDPSocket = None

flag = True
opponent_address_port = None

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    print(event, values)
    window["-ERROR-"].update("")

    try:
        port = int(values['-INPUT-'])
        if flag:
            UDPSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            UDPSocket.bind((IP, port))
            print("UDP socket created")
        else:
            opponent_address_port = ("127.0.0.1", port)
            break

        window['-TITLE-'].update('Choose opponent game port')
        window['-INPUT-'].update('5002')
        flag = False
    except Exception as e:
        print(str(e))
        window["-ERROR-"].update("Wrong port number")

window.close()

############################################################
UDPSocket.sendto(str.encode("start"), opponent_address_port)

colors = None

while True:
    try:
        move, adres = UDPSocket.recvfrom(bufSize)
        move = move.decode()
        print(move, adres)
        if move == "start":
            colors = get_random_colors()
            UDPSocket.sendto(str.encode(json.dumps(colors)),
                             opponent_address_port)
            break
        else:
            colors = json.loads(move)
            break

    except:
        time.sleep(1)

print(colors)

layout = [[sg.B(' ', size=(8, 4), key=(j, i), button_color="black")
           for i in range(6)] for j in range(4)]

window = sg.Window('Memory Game', layout)

# Event Loop
while True:
    event, values = window.read()
    print(event, values)
    if event in (None, 'Exit'):
        break
    # current_marker = window[event].get_text()
    # window[event].update('X' if current_marker ==
    #                      ' ' else 'O' if current_marker == 'X' else ' ')
    window[event].update(button_color=colors[event[0]][event[1]])
window.close()
