from copy import deepcopy
from random import randint
import math


class DDGame:
    def __init__(self):
        self.board = [Army(0, 0)] * 16
        self.white = Player()
        self.black = Player()

        roll = randint(1, 100)
        if roll > 50:
            self.current_player = self.white
        else:
            self.current_player = self.black

        self.is_destruction = False

    def deploy(self, player, pos, number):
        army = Army(player, number)

        if pos < 0 or pos > 16:
            return False
        if army.number <= 0 or army.number > 8:
            return False
        if self.board[pos].number != 0:
            return False

        self.board[pos] = army

        if army.player is self.white:
            self.white.remove(army.number)
        elif army.player is self.black:
            self.black.remove(army.number)

        self.swap_players()
        return True

    def destroy(self, player, pos):

        if pos < 0 or pos > 16:
            return False
        if self.board[pos].number == 0:
            return False
        if self.board[pos].player is player:
            return False
        if (
            self.board[(pos - 1) % 16].player is not player
            and self.board[(pos + 1) % 16].player is not player
        ):
            return False

        # Both left and right are the player's
        if (
            self.board[(pos - 1) % 16].player is player
            and self.board[(pos + 1) % 16].player is player
        ):
            if (
                self.board[(pos - 1) % 16].number + self.board[(pos - 1) % 16].number
                > self.board[pos].number
            ):
                self.board[pos] = Army(Player(), 0)
                self.swap_players()
                return True
            else:
                return False
        # Only the left is the player's
        elif (
            self.board[(pos - 1) % 16].player is player
            and self.board[(pos + 1) % 16].player is not player
        ):
            if self.board[(pos - 1) % 16].number > self.board[pos].number:
                self.board[pos] = Army(Player(), 0)
                self.swap_players()
                return True
            else:
                return False
        # Only the right is the player's
        elif (
            self.board[(pos - 1) % 16].player is not player
            and self.board[(pos + 1) % 16].player is player
        ):
            if self.board[(pos + 1) % 16].number > self.board[pos].number:
                self.board[pos] = Army(Player(), 0)
                self.swap_players()
                return True
            else:
                return False

    def decide_winner(self):
        armies_white = 0
        armies_black = 0
        for i in range(len(self.board)):
            if self.board[i].player is self.white:
                armies_white += 1
            elif self.board[i].player is self.black:
                armies_black += 1

        if armies_white > armies_black:
            # print("Winner is white.")
            return 1
        elif armies_white < armies_black:
            # print("Winner is black.")
            return 2
        else:
            sum_white = 0
            sum_black = 0
            for i in range(len(self.board)):
                if self.board[i].player is self.white:
                    sum_white += self.board[i].number
                elif self.board[i].player is self.black:
                    sum_black += self.board[i].number
            if sum_white > sum_black:
                # print("Winner is white.")
                return 1
            elif sum_white < sum_black:
                # print("Winner is black.")
                return 2
            else:
                # print("It's a draw.")
                return 3

    def create_children(self, player):
        children = []
        for i in range(len(self.board)):  # deployment phase
            for j in range(len(player.available)):
                if player is self.white:
                    if self.board[i].number == 0:
                        temp_state = deepcopy(self)
                        temp_state.deploy(
                            temp_state.white, i, temp_state.white.available[j]
                        )
                        if temp_state != self:
                            children.append(temp_state)
                elif player is self.black:
                    if self.board[i].number == 0:
                        temp_state = deepcopy(self)
                        temp_state.deploy(
                            temp_state.black, i, temp_state.black.available[j]
                        )
                        if temp_state != self:
                            children.append(temp_state)

        if len(self.white.available) == 0 and len(self.black.available) == 0:
            self.is_destruction = True

        if self.is_destruction:  # destruction phase
            for i in range(len(self.board)):
                if player is self.white:
                    temp_state = deepcopy(self)
                    temp_state.destroy(temp_state.white, i)
                    if temp_state != self:
                        children.append(temp_state)
                elif player is self.black:
                    temp_state = deepcopy(self)
                    temp_state.destroy(temp_state.black, i)
                    if temp_state != self:
                        children.append(temp_state)

        return children

    def evaluation_function(self):
        if self.is_destruction:  # destruction phase
            if self.is_end_state():
                who_wins = self.decide_winner()
                if who_wins == 1:
                    return 1
                elif who_wins == 2:
                    return -1
                elif who_wins == 3:
                    return 0
            else:
                return 0
        else:  # deployment phase
            value = 0
            for i in range(len(self.board)):
                if self.can_destroy(self.white, i):
                    value += 1
                elif self.can_destroy(self.black, i):
                    value -= 1
            return value

    def swap_players(self):
        if self.current_player is self.white:
            self.current_player = self.black
        elif self.current_player is self.black:
            self.current_player = self.white

    def can_destroy(self, player, pos):
        if pos < 0 or pos > 16:
            return False
        if self.board[pos].number == 0:
            return False
        if self.board[pos].player is player:
            return False
        if (
            self.board[(pos - 1) % 16].player is not player
            and self.board[(pos + 1) % 16].player is not player
        ):
            return False
        if (
            self.board[(pos - 1) % 16].player is player
            and self.board[(pos + 1) % 16].player is player
        ):
            if (
                self.board[(pos - 1) % 16].number + self.board[(pos - 1) % 16].number
                > self.board[pos].number
            ):
                return True
            else:
                return False
        elif (
            self.board[(pos - 1) % 16].player is player
            and self.board[(pos + 1) % 16].player is not player
        ):

            if self.board[(pos - 1) % 16].number > self.board[pos].number:
                return True
            else:
                return False
        elif (
            self.board[(pos - 1) % 16].player is not player
            and self.board[(pos + 1) % 16].player is player
        ):
            if self.board[(pos + 1) % 16].number > self.board[pos].number:
                return True
            else:
                return False

    # def generate_random_destruction_phase(self):
    #     while len(self.current_player.available) > 0:
    #         i = randint(0, 15)
    #         for j in self.current_player.available:
    #             self.deploy(self.current_player, i, j)

    def generate_random_destruction_phase(self):
        while len(self.current_player.available) > 0:
            i = randint(0, 15)
            for j in self.current_player.available:
                self.deploy(self.current_player, i, j)
        while True:
            temp_state = deepcopy(self)
            destroy_times = randint(1, 7)
            if destroy_times % 2 == 1:  # keep current_player the same after
                destroy_times += 1
            for _ in range(destroy_times):
                temp_state.board[randint(1, len(self.board) - 1)] = Army(Player(), 0)
            if not temp_state.is_end_state():
                self.__dict__.update(temp_state.__dict__)
                break

    def generate_hardest_destruction_phase(self):
        for i in range(len(self.board)):
            for j in self.current_player.available:
                self.deploy(self.current_player, i, j)

    def is_end_state(self):
        return len(self.create_children(self.current_player)) == 0

    # create a string representation of the object
    def __str__(self):
        board_copy = deepcopy(self.board)
        for i in range(len(self.board)):
            if type(self.board[i]) is Army:
                board_copy[i] = board_copy[i].number
        for i in range(len(board_copy)):
            if self.board[i].player is self.white:
                board_copy[i] = str(board_copy[i]) + "w"
            elif self.board[i].player is self.black:
                board_copy[i] = str(board_copy[i]) + "b"
            else:  # undefined player
                board_copy[i] = "  "
        return str(board_copy)

    def __eq__(self, other):
        if isinstance(other, DDGame):
            return self.__str__() == other.__str__()


class Army:
    def __init__(self, player, number):
        self.player = player
        self.number = number  # in range [1, 8]

    def __eq__(self, other):
        if isinstance(other, Army):
            return self.player is other.player and self.number == other.number


class Player:
    def __init__(self):
        self.available = list(range(1, 9))

    def remove(self, number):
        self.available.remove(number)
