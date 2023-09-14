"""
Tic Tac Toe Player
"""

import copy
import math
import random

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


# Checks the number of played moves.
def played_moves(board):
    played = 0
    for i in board:
        for j in i:
            if j != EMPTY:
                played += 1
    return played


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Calculates the number of played moves
    played = played_moves(board)

    # If played is even, it's X's turn
    if played % 2 == 0:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                action = (i, j)
                moves.add(action)
    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("Invalid Action!")

    board_copy = copy.deepcopy(board)
    board_copy[action[0]][action[1]] = player(board)
    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Checking vertical & horizontal
    for i in range(3):
        if board[0][0 + i] == board[1][0 + i] == board[2][0 + i] != EMPTY:
            return board[0][0 + i]
        elif board[0 + i][0] == board[0 + i][1] == board[0 + i][2] != EMPTY:
            return board[0 + i][0]

    # Checking diagonal
    if ((board[0][0] == board[1][1] == board[2][2]) or
            (board[0][2] == board[1][1] == board[2][0]) and
            (board[1][1] != EMPTY)):
        return board[1][1]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None or len(actions(board)) == 0:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board):
        if winner(board) == X:
            return 1
        elif winner(board) == O:
            return -1
        else:
            return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    current_player = player(board)

    # If the computer is first, randomises the move to reduce processing time.
    if played_moves(board) == 0:
        return (random.randint(0, 2), random.randint(0, 2))
    else:
        # If player is X, maximise
        if current_player == X:
            return max_value(board)[1]
        # If player is O, minimise
        else:
            return min_value(board)[1]


# Finds move with maximum utility value 1.
def max_value(board):
    v = float('-inf')
    move = ()
    if terminal(board):
        return [utility(board), None]
    for action in actions(board):
        if min_value(result(board, action))[0] > v:
            move = action
        v = max(v, min_value(result(board, action))[0])
        # Ends loop if maximum value found.
        if v == 1:
            return [v, move]
    return [v, move]


# Finds move with minimum utility value -1.
def min_value(board):
    v = float('inf')
    move = ()
    if terminal(board):
        return [utility(board), None]
    for action in actions(board):
        if max_value(result(board, action))[0] < v:
            move = action
        v = min(v, max_value(result(board, action))[0])
        # Ends loop if minimum value found.
        if v == -1:
            return [v, move]
    return [v, move]
