import PySimpleGUI as sg
from colors import get_random_colors
import socket
import time
import json


def connect():
    sg.theme('Dark Blue 3')

    layout = [[sg.Text('Choose your game port', key='-TITLE-')],
              [sg.Input(default_text="5001", key="-INPUT-")],
              [sg.Text('', key='-ERROR-')],
              [sg.Button('OK', bind_return_key=True), sg.Exit()]]

    window = sg.Window('Game setup', layout)

    IP = "127.0.0.1"
    bufSize = 1024
    UDPSocket = None

    flag = True
    opponent_address_port = None

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            window.close()
            exit()
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

    # list of randomized pair colors made by player that joined first
    colors = None
    # determines if it is player turn to play
    turn = False

    while True:
        try:
            move, adres = UDPSocket.recvfrom(bufSize)
            move = move.decode()
            if move == "start":
                colors = get_random_colors()
                UDPSocket.sendto(str.encode(json.dumps(colors)),
                                 opponent_address_port)
                turn = True
                break
            else:
                colors = json.loads(move)
                break
        except:
            time.sleep(1)

    return {
        "UDPSocket": UDPSocket,
        "bufSize": bufSize,
        "turn": turn,
        "colors": colors,
        "opponent_address_port": opponent_address_port
    }
