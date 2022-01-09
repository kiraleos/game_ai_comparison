import math


class Gametree:
    def __init__(self, start_state, max_depth):
        self.start_state = start_state
        self.max_depth = max_depth
        self.eval_ctr = 0
        self.prune_ctr = 0
        self.depth_ctr = 0

    def best_move_minimax(self, state, max_depth, player):
        if player is state.white:
            moves = []
            values = []
            moves = state.create_children(state.current_player)
            for i in range(len(moves)):
                values.append(
                    self.minimax(moves[i], max_depth, moves[i].current_player)
                )

            return moves[values.index(max(values))]
        elif player is state.black:
            moves = state.create_children(state.current_player)
            values = []
            for i in range(len(moves)):
                values.append(
                    self.minimax(moves[i], max_depth, moves[i].current_player)
                )

            return moves[values.index(min(values))]

    def best_move_alphabeta(self, state, max_depth, alpha, beta, player):
        if player is state.white:
            moves = state.create_children(state.current_player)
            values = []
            for i in range(len(moves)):
                values.append(
                    self.alphabeta(
                        moves[i], max_depth, alpha, beta, moves[i].current_player
                    )
                )

            return moves[values.index(max(values))]
        elif player is state.black:
            moves = state.create_children(state.current_player)
            values = []
            for i in range(len(moves)):
                values.append(
                    self.alphabeta(
                        moves[i], max_depth, alpha, beta, moves[i].current_player
                    )
                )

            return moves[values.index(min(values))]

    def minimax(self, state, max_depth, player):
        if 10000 - max_depth > self.depth_ctr:
            self.depth_ctr = 10000 - max_depth
        if max_depth == 0 or state.is_end_state():
            self.eval_ctr += 1
            return state.evaluation_function()

        if player is state.white:  # maximizing player
            value = -math.inf
            for move in state.create_children(state.current_player):
                value = max(
                    value, self.minimax(move, max_depth - 1, move.current_player)
                )
            return value
        elif player is state.black:  # minimizing player
            value = math.inf
            for move in state.create_children(state.current_player):
                value = max(
                    value, self.minimax(move, max_depth - 1, move.current_player)
                )
            return value

    def alphabeta(self, state, max_depth, alpha, beta, player):
        if 10000 - max_depth > self.depth_ctr:
            self.depth_ctr = 10000 - max_depth
        if max_depth == 0 or state.is_end_state():
            self.eval_ctr += 1
            return state.evaluation_function()

        if player is state.white:  # maximizing player
            value = -math.inf
            for move in state.create_children(state.current_player):
                value = max(
                    value,
                    self.alphabeta(
                        move, max_depth - 1, alpha, beta, move.current_player
                    ),
                )
                alpha = max(alpha, value)
                if alpha >= beta:
                    self.prune_ctr += 1
                    break
            return value
        elif player is state.black:  # minimizing player
            value = math.inf
            for move in state.create_children(state.current_player):
                value = min(
                    value,
                    self.alphabeta(
                        move, max_depth - 1, alpha, beta, move.current_player
                    ),
                )
                beta = min(beta, value)
                if alpha >= beta:
                    self.prune_ctr += 1
                    break
            return value
