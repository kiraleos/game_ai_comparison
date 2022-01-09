from Gametree import Gametree
from DDGame import DDGame
from IsolaGame import IsolaGame
import math
import time


def main():
    # state = DDGame()
    # state.generate_random_destruction_phase()
    state = IsolaGame(4)
    state.generate_random_state()
    one_move("alphabeta", 10000, state)
    one_move("minimax", 10000, state)
    # cpu_vs_cpu("alphabeta", 10000, state)
    # cpu_vs_cpu("minimax", 10000, state)


def human_vs_cpu(algorithm, max_depth):
    state = DDGame()
    game = Gametree(state, max_depth - 1)
    if algorithm == "alphabeta":
        while not game.start_state.is_end_state():
            if game.start_state.current_player == game.start_state.white:
                print("Your turn.")
                if game.start_state.is_destruction:
                    print("Type position [1, 16] to destroy.")
                    string = int(input()) - 1
                    game.start_state.destroy(game.start_state.current_player, string)
                else:
                    print(
                        "Type position [1, 16] and army number [1, 8] to deploy separated by space."
                    )
                    string = input()
                    tokens = string.split()
                    game.start_state.deploy(
                        game.start_state.current_player,
                        int(tokens[0]) - 1,
                        int(tokens[1]),
                    )
            print("CPU's turn.")
            game.start_state = game.best_move_alphabeta(
                game.start_state,
                game.max_depth,
                -math.inf,
                math.inf,
                game.start_state.current_player,
            )
            print(game.start_state)
    elif algorithm == "minimax":
        while not game.start_state.is_end_state():
            if game.start_state.current_player == game.start_state.white:
                print("Your turn.")
                if game.start_state.is_destruction:
                    print("Type position [1, 16] to destroy.")
                    string = int(input()) - 1
                    game.start_state.destroy(game.start_state.current_player, string)
                else:
                    print(
                        "Type position [1, 16] and army number [1, 8] to deploy separated by space."
                    )
                    string = input()
                    tokens = string.split()
                    game.start_state.deploy(
                        game.start_state.current_player,
                        int(tokens[0]) - 1,
                        int(tokens[1]),
                    )
            print("CPU's turn.")
            game.start_state = game.best_move_minimax(
                game.start_state, game.max_depth, game.start_state.current_player
            )
            print(game.start_state)

    who_wins = game.start_state.decide_winner()
    if who_wins == 1:
        print("You win.")
    elif who_wins == 2:
        print("CPU wins.")
    elif who_wins == 3:
        print("It's a draw.")


def cpu_vs_cpu(algorithm, max_depth, state):
    start_time = time.perf_counter()
    game = Gametree(state, max_depth - 1)
    if algorithm == "alphabeta":
        print("\nAlphabeta: \n")
    else:
        print("\nMinimax: \n")
    print(game.start_state)
    if algorithm == "alphabeta":
        while not game.start_state.is_end_state():
            game.start_state = game.best_move_alphabeta(
                game.start_state,
                game.max_depth,
                -math.inf,
                math.inf,
                game.start_state.current_player,
            )
            print(game.start_state)
    elif algorithm == "minimax":
        while not game.start_state.is_end_state():
            game.start_state = game.best_move_minimax(
                game.start_state, game.max_depth, game.start_state.current_player
            )
            print(game.start_state)

    end_time = time.perf_counter()
    who_wins = game.start_state.decide_winner()
    if who_wins == 1:
        print("    \nWhite wins.")
    elif who_wins == 2:
        print("    \nBlack wins.")
    elif who_wins == 3:
        print("    \nIt's a draw.")

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"\n    Time elapsed: {elapsed_time:0.3f} seconds")
    print(f"    Max depth reached: {game.depth_ctr}")
    print(f"    Leaf nodes evaluated: {game.eval_ctr}")
    if algorithm == "alphabeta":
        print(f"    Branches pruned: {game.prune_ctr}")


def one_move(algorithm, max_depth, state):
    start_time = time.perf_counter()
    game = Gametree(state, max_depth - 1)
    if algorithm == "alphabeta":
        print("\nAlphabeta: \n")
    else:
        print("\nMinimax: \n")
    print(game.start_state)
    if algorithm == "alphabeta":
        game.start_state = game.best_move_alphabeta(
            game.start_state,
            game.max_depth,
            -math.inf,
            math.inf,
            game.start_state.current_player,
        )
        print(game.start_state)
    elif algorithm == "minimax":
        game.start_state = game.best_move_minimax(
            game.start_state, game.max_depth, game.start_state.current_player
        )
        print(game.start_state)

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"\n    Time elapsed: {elapsed_time:0.3f} seconds")
    print(f"    Max depth reached: {game.depth_ctr}")
    print(f"    Leaf nodes evaluated: {game.eval_ctr}")
    if algorithm == "alphabeta":
        print(f"    Branches pruned: {game.prune_ctr}")


if __name__ == "__main__":
    main()
