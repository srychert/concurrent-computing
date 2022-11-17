class Game:
    def __init__(self, player, board):
        temp = board if board != "" else "_|_|_\n"*3
        self.board = [r.split("|") for r in temp.split("\n")][:-1]
        self.player = player

    def make_move(self):
        move = input("Play a move (x,y): ")
        x, y = move.spit(",")
        self.board[int(x)][int(y)] = self.player

    def get_board(self):
        return self.board
