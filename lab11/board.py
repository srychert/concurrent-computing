import PySimpleGUI as sg
from colors import get_random_colors
import struct
import socket
import time
import json
import queue
import threading

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

# randomazied list of pair colors made by pplayer that first joins
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

########################################################################


def long_operation_thread(gui_queue):
    """
    A worker thread that communicates with the GUI through a queue
    This thread can block for as long as it wants and the GUI will not be affected
    :param gui_queue: (queue.Queue) Queue to communicate back to GUI that task is completed
    :return:
    """
    print("Starting thread")
    move, adres = UDPSocket.recvfrom(bufSize)
    gui_queue.put(move.decode())  # put a move into queue for GUI


# queue used to communicate between the gui and the threads
gui_queue = queue.Queue()

layout = [[sg.Text('Your turn' if turn else "Opponent turn", key='-TITLE-'), sg.Text("Points: 0", key='-POINTS-')],
          [[sg.B(' ', size=(8, 4), key=(j, i), button_color="black", disabled=not turn)
           for i in range(6)] for j in range(4)]]

window = sg.Window('Memory Game', layout)


def update_gui():
    window["-TITLE-"].update('Your turn' if turn else "Opponent turn")
    for i in range(6):
        for j in range(4):
            window[(j, i)].update(disabled=not turn)


points = 0
moves_remaining = 2
thread_flag = True

# Event Loop
while True:
    event, values = window.Read(timeout=100)
    if (event != "__TIMEOUT__"):
        print(event, values)
        print(moves_remaining, turn, thread_flag)
    if event in (None, 'Exit'):
        break

    # player move
    if turn and type(event) is tuple:
        if moves_remaining > 0:
            window[event].update(button_color=colors[event[0]][event[1]])
            moves_remaining -= 1
            UDPSocket.sendto(str.encode(json.dumps({"move": event, "next": False})),
                             opponent_address_port)
        if moves_remaining == 0:
            turn = False
            update_gui()

            UDPSocket.sendto(str.encode(json.dumps({"move": None, "next": True})),
                             opponent_address_port)
    # start threads to get moves form other player
    if not turn and thread_flag:
        for _ in range(3):
            threading.Thread(target=long_operation_thread,
                             args=(gui_queue,), daemon=True).start()
        thread_flag = False

    # --------------- Check for incoming moves from threads  ---------------
    try:
        move = gui_queue.get_nowait()
        move = json.loads(move)
    except queue.Empty:             # get_nowait() will get exception when Queue is empty
        move = None              # break from the loop if no more moves are queued up

    # if move received from queue, display the move in the Window
    if move:
        print('Got a move back from the thread: ')
        print(move)
        tile = move["move"]
        if tile != None:
            # make list hashable by turning it into a tuple
            tile = tuple(tile)
            window[tile].update(button_color=colors[tile[0]][tile[1]])

        if move["next"]:
            turn = True
            thread_flag = True
            moves_remaining = 2
            update_gui()

window.close()
