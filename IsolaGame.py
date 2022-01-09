from random import randint, normalvariate
from copy import deepcopy, copy
from prettytable import PrettyTable
from prettytable import ALL


class IsolaGame:
    def __init__(self, size):
        self.size = size
        self.board = [[" " for i in range(size)] for j in range(size)]
        self.white = "w"
        self.black = "b"
        self.winner = "undecided"

        roll = randint(1, 100)
        if roll > 50:
            self.current_player = self.white
        else:
            self.current_player = self.black

        self.init_board()

    def move(self, player, x, y):
        if not self.can_move(x, y):
            return False

        prev_x, prev_y = self.get_position(player)
        self.board[prev_x][prev_y] = " "
        self.board[x][y] = player
        return True

    def block(self, x, y):
        if not self.can_move(x, y):
            return False

        self.board[x][y] = "x"
        self.swap_players()
        return True

    def can_move(self, x, y):
        size = self.size
        if x < 0 or x >= size or y < 0 or y >= size:
            return False
        if self.board[x][y] == " ":
            return True

    def get_position(self, player):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == player:
                    return [i, j]
        return False

    def create_children(self, player):
        children = []
        for off_x in range(-1, 2):
            for off_y in range(-1, 2):
                temp_state1 = deepcopy(self)
                curr_x, curr_y = self.get_position(player)
                temp_state1.move(player, curr_x + off_x, curr_y + off_y)
                if temp_state1.board != self.board:
                    for i in range(self.size):
                        for j in range(self.size):
                            temp_state = deepcopy(temp_state1)
                            temp_state.block(i, j)
                            if temp_state.board != temp_state1.board:
                                children.append(temp_state)

        return children

    def evaluation_function(self):
        value = 0
        for off_x in range(-1, 2):
            for off_y in range(-1, 2):
                temp_state = deepcopy(self)
                curr_x, curr_y = self.get_position(self.white)
                temp_state.move(self.white, curr_x + off_x, curr_y + off_y)
                if temp_state.board != self.board:
                    value += 1
        for off_x in range(-1, 2):
            for off_y in range(-1, 2):
                temp_state = deepcopy(self)
                curr_x, curr_y = self.get_position(self.black)
                temp_state.move(self.black, curr_x + off_x, curr_y + off_y)
                if temp_state.board != self.board:
                    value -= 1
        return value

    def is_end_state(self):
        if len(self.create_children(self.current_player)) == 0:
            if self.current_player == self.white:
                self.winner = self.black
            else:
                self.winner = self.white
            return True
        else:
            return False

    def decide_winner(self):
        if self.winner == self.white:
            return 1
        elif self.winner == self.black:
            return 2

    def swap_players(self):
        if self.current_player is self.white:
            self.current_player = self.black
        elif self.current_player is self.black:
            self.current_player = self.white

    def init_board(self):
        while True:
            i = randint(0, self.size - 1)
            j = randint(0, self.size - 1)
            if self.board[i][j] == " ":
                break
        self.board[i][j] = self.white

        while True:
            i = randint(0, self.size - 1)
            j = randint(0, self.size - 1)
            if self.board[i][j] == " ":
                break
        self.board[i][j] = self.black

    def generate_random_state(self):
        moves = round(normalvariate(((self.size * self.size * 1.2)) / 2, self.size))
        for _ in range(moves):
            while True:
                x = randint(0, self.size)
                y = randint(0, self.size)
                if self.can_move(x, y):
                    self.block(x, y)
                    break

    def __str__(self):
        p = PrettyTable()
        board_copy = copy(self.board)
        for row in board_copy:
            for i in range(len(row)):
                if row[i] == "x":
                    pass
            p.add_row(row)
        p.hrules = ALL

        return p.get_string(header=False, border=True)
