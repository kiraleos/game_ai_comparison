from random import randint


class ConnectFourGame:
    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y
        self.board = [["O" for _ in range(size_y)] for _ in range(size_x)]
        self.white = "P"
        self.black = "S"
        self.winner = "undecided"

        self.is_end = False

        self.current_player = self.white

    def play(self, player, y):
        if self.board[0][y] != "O":
            return False
        x = 0
        while x < self.size_x and self.board[x][y] == "O":
            x += 1
        self.board[x - 1][y] = player
        self.swap_players()

    def create_children(self, player):
        children = []
        for y in range(self.size_y):
            temp_state = copy_game(self)
            temp_state.play(player, y)
            if temp_state.board != self.board:
                children.append(temp_state)

        if len(children) == 0:
            self.is_end = True
        return children

    def evaluation_function(self):
        # maximizing player
        if not self.is_end:
            if self.check_win(self.white):
                self.winner = self.white
                return 1
            # minimizing player
            if self.check_win(self.black):
                self.winner = self.black
                return -1

        # add proper evaluation function here instead of returning 0
        return 0

    def check_win(self, player):
        t = player
        a = self.board
        for i in range(self.size_x):
            for j in range(self.size_y):
                try:
                    if (
                        a[i][j] == t
                        and a[i][j + 1] == t
                        and a[i][j + 2] == t
                        and a[i][j + 3] == t
                    ):
                        return True
                except IndexError:
                    next
        for i in range(self.size_x):
            for j in range(self.size_y):
                try:
                    if (
                        a[i][j] == t
                        and a[i + 1][j] == t
                        and a[i + 2][j] == t
                        and a[i + 3][j] == t
                    ):
                        return True
                except IndexError:
                    next

        for i in range(self.size_x):
            for j in range(self.size_y):
                try:
                    if (
                        a[i][j] == t
                        and a[i - 1][j] == t
                        and a[i - 2][j] == t
                        and a[i - 3][j] == t
                    ):
                        return True
                except IndexError:
                    next
        for i in range(self.size_x):
            for j in range(self.size_y):
                try:
                    if (
                        a[i][j] == t
                        and a[i][j - 1] == t
                        and a[i][j - 2] == t
                        and a[i][j - 3] == t
                    ):
                        return True
                except IndexError:
                    next
        for i in range(self.size_x):
            for j in range(self.size_y):
                try:
                    if (
                        a[i][j] == t
                        and a[i - 1][j + 1] == t
                        and a[i - 2][j + 2] == t
                        and a[i - 3][j + 3] == t
                    ):
                        return True
                except IndexError:
                    next
        for i in range(self.size_x):
            for j in range(self.size_y):
                try:
                    if (
                        a[i][j] == t
                        and a[i + 1][j + 1] == t
                        and a[i + 2][j + 2] == t
                        and a[i + 3][j + 3] == t
                    ):
                        return True
                except IndexError:
                    next
        for i in range(self.size_x):
            for j in range(self.size_y):
                try:
                    if (
                        a[i][j] == t
                        and a[i - 1][j - 1] == t
                        and a[i - 2][j - 2] == t
                        and a[i - 3][j - 3] == t
                    ):
                        return True
                except IndexError:
                    next
        for i in range(self.size_x):
            for j in range(self.size_y):
                try:
                    if (
                        a[i][j] == t
                        and a[i - 1][j - 1] == t
                        and a[i - 2][j - 2] == t
                        and a[i - 3][j - 3] == t
                    ):
                        return True
                except IndexError:
                    next
        return False

    def is_end_state(self):
        return self.is_end or self.check_win(self.white) or self.check_win(self.black)

    def swap_players(self):
        if self.current_player is self.white:
            self.current_player = self.black
        elif self.current_player is self.black:
            self.current_player = self.white

    def decide_winner(self):
        if self.winner == self.white:
            return 1
        if self.winner == self.black:
            return 2
        if self.winner == "undecided":
            return 3

    def generate_random_state(self):
        moves = 10
        for _ in range(moves):
            while True:
                y = randint(0, self.size_y - 1)
                self.play(self.current_player, y)
                break

    def __str__(self):
        return str(
            "\n".join([" ".join([str(cell) for cell in row]) for row in self.board])
            + "\n"
        )


def copy_game(game: ConnectFourGame):
    a = ConnectFourGame(game.size_x, game.size_y)
    a.board = [x[:] for x in game.board]
    a.winner = game.winner
    a.current_player = game.current_player
    return a
