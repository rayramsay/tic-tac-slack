import json

sb1 = "[[null, null, null], [null, null, null], [null, null, null]]"
sb2 = '[[null, "O", null], ["O", "X", null], [null, "O", "X"]]'


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

print format_board(sb1)
print format_board(sb2)
