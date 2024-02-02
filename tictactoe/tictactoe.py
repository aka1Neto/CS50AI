"""
Tic Tac Toe Player
"""

import copy
import math

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


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    turn = sum(row.count(EMPTY) for row in board);
    if turn == 0:
        return None;

    elif turn % 2 == 0:
        return O;

    else:
        return X;


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action = set();

    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == EMPTY:
                action.add((i, j));

    return action;


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise ValueError;

    result = copy.deepcopy(board);
    result[action[0]][action[1]] = player(board);
    return result;


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    if [X, X, X] in board:
        return X;

    if [O, O, O] in board:
        return O;

    for j in range(len(board)):
        if all(board[0][j] == board[i][j] for i in range(len(board))):
            return board[0][j];

    if all(board[0][0] == board[i][i] for i in range(len(board))) or all(board[0][2] == board[i][2 - i] for i in range(len(board))):
        return board[1][1];

    return None;



def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if sum(row.count(EMPTY) for row in board) == 0 or winner(board):
        return True;

    else:
        return False;


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board):
        if winner(board) == X:
            return 1;

        elif winner(board) == O:
            return -1;

        else:
            return 0;


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None;

    if player(board) == X:
        _, move = max_value(board);
        return move;

    else:
        _, move = min_value(board);
        return move;


def max_value(board):
    if terminal(board):
        return utility(board), None;

    max_value = float("-inf");
    move = None;
    for action in actions(board):
        value, _ = min_value(result(board, action));
        if value == 1:
            return value, action;

        if value > max_value:
            max_value = value;
            move = action;

    return max_value, move;

def min_value(board):
    if terminal(board):
        return utility(board), None;


    min_value = float("inf");
    move = None;
    for action in actions(board):
        value, _ = max_value(result(board, action));
        if value == -1:
            return value, action;

        if value < min_value:
            min_value = value;
            move = action;

    return min_value, move;