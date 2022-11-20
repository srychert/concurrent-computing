class Game:
    def __init__(self, player, board):
        temp = board if board != "" else "_|_|_\n"*3
        self.board = [r.split("|") for r in temp.split("\n")][:-1]
        self.player = player

    def get_board(self):
        board = ""
        for r in self.board:
            board += "|".join(r) + "\n"

        return board

    def make_move(self):
        moves = [0, 1, 2]
        # lost = self.check_win("O" if self.player == "X" else "X")

        # if lost is not None:
        #     return lost

        while True:
            move = input("Play a move (x,y): ")

            x, y = move.split(",")
            try:
                x = int(x)
                y = int(y)

                if (x not in moves or y not in moves):
                    raise

                if (self.board[x][y] != "_"):
                    raise

                self.board[x][y] = self.player
                win = self.check_win(self.player)
                print(win)
                return win
            except:
                print("Bad move")

    def check_win(self, player):
        for r in self.board:
            if self.all_same(player, r):
                return True

        for column in zip(*self.board):
            if self.all_same(player, column):
                return True

        # first diagonal
        if self.all_same(player, [self.board[i][i] for i in range(len(self.board))]):
            return True

        # second diagonal
        if self.all_same(player, [self.board[i][len(self.board)-i-1] for i in range(len(self.board))]):
            return True

        return False

    def all_same(self, ele, iterator):
        iterator = iter(iterator)
        return all(ele == x for x in iterator)
