import PySimpleGUI as sg
import time
import json
import queue
import threading
from Game import Game
from msg import msg
from connect import connect

params = connect()
UDPSocket = params["UDPSocket"]
bufSize = params["bufSize"]
turn = params["turn"]
colors = params["colors"]
opponent_address_port = params["opponent_address_port"]
########################################################################


def long_operation_thread(gui_queue):
    """
    A worker thread that communicates with the GUI through a queue
    This thread can block for as long as it wants and the GUI will not be affected
    :param gui_queue: (queue.Queue) Queue to communicate back to GUI that task is completed
    :return:
    """
    print("Starting thread")
    try:
        move, adres = UDPSocket.recvfrom(bufSize)
        gui_queue.put(move.decode())  # put a move into queue for GUI
    except Exception as e:
        print(str(e))


# queue used to communicate between the gui and the threads
gui_queue = queue.Queue()

sg.theme('Dark Blue 3')

layout = [[sg.Text('Your turn' if turn else "Opponent turn", key='-TITLE-'), sg.Text("Points: 0", key='-POINTS-')],
          [[sg.Button(' ', size=(8, 4), key=(j, i), button_color="black", disabled=not turn, focus=False, highlight_colors=None)
           for i in range(6)] for j in range(4)]]

window = sg.Window('Memory Game', layout)

points = 0
opponent_points = 0
moves_remaining = 2
thread_flag = True
game = Game(colors)


def update_text(title=None):
    if title is not None:
        window["-TITLE-"].update(title)
    else:
        window["-TITLE-"].update('Your turn' if turn else "Opponent turn")
    window["-POINTS-"].update(
        f"Points: {points} \t Opponent points: {opponent_points}")


def update_buttons(disabled=None):
    for i in range(6):
        for j in range(4):
            window[(j, i)].update(
                disabled=disabled if disabled is not None else not turn)


def update_gui():
    update_text()
    update_buttons()


def make_threads(n):
    for _ in range(n):
        threading.Thread(target=long_operation_thread,
                         args=(gui_queue,), daemon=True).start()


def hide_cards(cards):
    time.sleep(1)
    for card in cards:
        window[tuple(card)].update(button_color="black")


def get_end_msg():
    if points > opponent_points:
        return "win"
    elif points < opponent_points:
        return "lose"
    return "tie"


# Event Loop
while True:
    event, values = window.Read(timeout=100)
    if (event != "__TIMEOUT__"):
        print(event, values)
    if event in (None, 'Exit'):
        UDPSocket.sendto(str.encode(json.dumps(msg(abandon=True))),
                         opponent_address_port)
        break

    # player move
    if turn and type(event) is tuple:
        # ignore already paired tiles and played moves
        if game.check_before_play(event):
            print("move already played")
            continue

        if moves_remaining > 0:
            game.add(event)
            window[event].update(button_color=colors[event[0]][event[1]])
            moves_remaining -= 1
            UDPSocket.sendto(str.encode(json.dumps(msg(move=event))),
                             opponent_address_port)

        if moves_remaining == 0:
            played_moves = tuple(game.get_moves())
            outcome = game.play()

            # grant point
            if outcome:
                points += 1
                update_text()
                moves_remaining = 2
                UDPSocket.sendto(str.encode(json.dumps(msg(point=True, cards=played_moves))),
                                 opponent_address_port)
            else:
                # hide cards
                threading.Thread(target=hide_cards,
                                 args=(played_moves,), daemon=True).start()

                # uppdate for next turn
                turn = False
                update_gui()
                UDPSocket.sendto(str.encode(json.dumps(msg(next=True, cards=played_moves))),
                                 opponent_address_port)

            if game.is_finished():
                update_text(title=f"Game over, you {get_end_msg()}!")
                update_buttons(disabled=True)
    # start threads to get moves form other player
    if not turn and thread_flag:
        make_threads(3)
        thread_flag = False

    # --------------- Check for incoming moves from threads  ---------------
    try:
        move = gui_queue.get_nowait()
        move = json.loads(move)
    except queue.Empty:             # get_nowait() will get exception when Queue is empty
        move = None              # break from the loop if no more moves are queued up

    # handle the move received from queue
    if move:
        print('Got a move back from the thread: ')
        print(move)
        tile = move["move"]
        if tile != None:
            # make list hashable by turning it into a tuple
            tile = tuple(tile)
            window[tile].update(button_color=colors[tile[0]][tile[1]])

        if move["point"]:
            opponent_points += 1
            update_text()

            for card in move["cards"]:
                game.set_as_revealed(tuple(card))

            if game.is_finished():
                update_text(title=f"Game over, you {get_end_msg()}!")
                update_buttons(disabled=True)

            make_threads(3)

        if move["next"]:
            threading.Thread(target=hide_cards,
                             args=(move["cards"],), daemon=True).start()
            turn = True
            thread_flag = True
            moves_remaining = 2
            time.sleep(1)
            update_gui()

        if move["abandon"]:
            update_text(title="Game abandoned")
            update_buttons(disabled=True)

window.close()
