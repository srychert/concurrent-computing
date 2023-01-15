from colors import get_random_colors
from itertools import groupby


def all_equal(iterable):
    g = groupby(iterable)
    return next(g, True) and not next(g, False)


class Game:
    def __init__(self, board):
        self.board = board
        self.cards_count = len(board) * len(board[0])
        self.revealed = set()
        self.current_moves = set()

    def check_before_play(self, move):
        return move in self.revealed or move in self.current_moves

    def add(self, move):
        self.current_moves.add(move)

    def set_as_revealed(self, card):
        self.revealed.add(card)

    def play(self):
        cards = []
        for x, y in self.current_moves:
            cards.append(self.board[x][y])

        eq = all_equal(cards)
        if eq:
            self.revealed.update(self.current_moves)

        self.current_moves.clear()
        return eq

    def is_finished(self):
        return self.cards_count == len(self.revealed)

    def get_moves(self):
        return self.current_moves.copy()
