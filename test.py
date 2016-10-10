import json

sb1 = "[[null, null, null], [null, null, null], [null, null, null]]"
sb2 = '[[null, "O", null], ["O", "X", null], ["X", "X", "X"]]'
sb3 = '[["X", "O", null], ["X", "X", null], ["X", "O", "X"]]'

def format_board(string_board):
    board = json.loads(string_board)
    formatted_board = ""
    for i in range(len(board)):
        formatted_board += "|"
        for item in board[i]:
            formatted_board += " "
            if not item:
                formatted_board += " "
            else:
                formatted_board += item
            formatted_board += " |"
        formatted_board += "\n"
        if i < len(board) - 1:
            formatted_board += "|---+---+---|\n"
    return formatted_board


def update(move, board):
        """Marks specified space."""

        board = json.loads(board)
        squares = {"a1": board[0][0], "a2": board[0][1], "a3": board[0][2],
                   "b1": board[1][0], "b2": board[1][1], "b3": board[1][2],
                   "c1": board[2][0], "c2": board[2][1], "c3": board[2][2]}

        mark = 'O'

        squares[move] = mark

        board = [[squares["a1"], squares["a2"], squares["a3"]],
                 [squares["b1"], squares["b2"], squares["b3"]],
                 [squares["c1"], squares["c2"], squares["c3"]]]

        return json.dumps(board)


def is_solved(board):
    """Checks whether the game has been won, and updates to inactive if so."""

    board = json.loads(board)

    # Check rows and columns.
    for i in xrange(3):
        if board[i][0] == board[i][1] == board[i][2] is not None \
        or board[0][i] == board[1][i] == board[2][i] is not None:
            return True

    return False

print is_solved(sb1)
print is_solved(sb2)
print is_solved(sb3)
