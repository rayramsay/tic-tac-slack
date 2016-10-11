from flask_sqlalchemy import SQLAlchemy
import random
import json

db = SQLAlchemy()


class Game(db.Model):
    """Game object."""

    __tablename__ = "games"

    game_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    channel_id = db.Column(db.String(64), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    player1_id = db.Column(db.String(64), nullable=False)
    player2_id = db.Column(db.String(64), nullable=False)
    active_player = db.Column(db.String(64), nullable=True)
    board = db.Column(db.String(128), nullable=False, default="[[null, null, null], [null, null, null], [null, null, null]]")
    winner = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        """Provides a human-readable representation of an instance of a game."""

        return "<Game id=%s channel_id=%s player1_id=%s player2_id=%s active_player=%s board=%s active=%s winner=%s>" % \
            (self.game_id,
             self.channel_id,
             self.player1_id,
             self.player2_id,
             self.active_player,
             self.board,
             self.active,
             self.winner)

    @classmethod
    def create(cls, channel_id, player1_id, player2_id):
        """Creates a new game in the database."""

        active_player = random.choice([player1_id, player2_id])
        game = cls(channel_id=channel_id, player1_id=player1_id, player2_id=player2_id, active_player=active_player)
        db.session.add(game)
        db.session.commit()

    @classmethod
    def get_by_channel(cls, channel_id):
        """Given a channel id, queries database for active game and returns game
        object if available."""

        return cls.query.filter(cls.channel_id == channel_id, cls.active.is_(True)).first()

    def format_board(self):
        """Takes board stored as JSON string and formats it for display in chat."""

        board = json.loads(self.board)
        formatted_board = ""
        for i in xrange(len(board)):
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

    def display_board(self, response_type, situation="ongoing"):
        """Creates either an ephemeral or an in_channel response with the
        formatted board and other information appropriate to the situation."""

        formatted_board = self.format_board()

        if situation == "ongoing":
            response = {
                "response_type": response_type,
                "text": "It's <@{}>'s turn!\n```{}```".format(self.active_player, formatted_board)
                }
        elif situation == "solved":
            response = {
                "response_type": response_type,
                "text": "<@{}> won!\n```{}```".format(self.winner, formatted_board)
                }
        elif situation == "draw":
            response = {
                "response_type": response_type,
                "text": "It's a draw!\n```{}```".format(formatted_board)
            }
        else:
            response = {
                "response_type": response_type,
                "text": "```{}```".format(formatted_board)
            }

        return response

    def is_legal(self, move):
        """Checks that the space the user wants to mark is unoccupied."""

        board = json.loads(self.board)
        squares = {"a1": board[0][0], "a2": board[0][1], "a3": board[0][2],
                   "b1": board[1][0], "b2": board[1][1], "b3": board[1][2],
                   "c1": board[2][0], "c2": board[2][1], "c3": board[2][2]}

        # If the square is occupied (i.e., not None), it's not a legal move.
        if squares[move]:
            return False

        return True

    def mark(self, move):
        """Marks specified space."""

        board = json.loads(self.board)
        squares = {"a1": board[0][0], "a2": board[0][1], "a3": board[0][2],
                   "b1": board[1][0], "b2": board[1][1], "b3": board[1][2],
                   "c1": board[2][0], "c2": board[2][1], "c3": board[2][2]}

        if self.active_player == self.player1_id:
            mark = 'X'
        else:
            mark = 'O'

        squares[move] = mark

        board = [[squares["a1"], squares["a2"], squares["a3"]],
                 [squares["b1"], squares["b2"], squares["b3"]],
                 [squares["c1"], squares["c2"], squares["c3"]]]

        self.board = json.dumps(board)

        db.session.commit()

    def swap_active_player(self):
        """Switches the active player."""

        if self.active_player == self.player1_id:
            self.active_player = self.player2_id
        else:
            self.active_player = self.player1_id

        db.session.commit()

    def is_solved(self):
        """Checks whether the game has been won and records winner if applicable."""

        board = json.loads(self.board)
        solved = False

        # Check rows and columns.
        for i in xrange(3):
            if board[i][0] == board[i][1] == board[i][2] is not None \
            or board[0][i] == board[1][i] == board[2][i] is not None:
                solved = True

        # Check diagonals.
        if board[0][0] == board[1][1] == board[2][2] is not None \
        or board[0][2] == board[1][1] == board[2][0] is not None:
            solved = True

        if solved:
            self.winner = self.active_player
            db.session.commit()

        return solved

    def is_draw(self):
        """Naively declares a draw by checking that every square has been filled."""

        board = json.loads(self.board)
        for i in xrange(3):
            for j in xrange(3):
                if board[i][j] is None:
                    return False
        return True

    def archive(self):
        """Switches the game's status to inactive so that a new game can be played."""

        self.active = False
        db.session.commit()


################################################################################

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ttt'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

################################################################################

if __name__ == "__main__":

    # If we run this module interactively, we can work with the database directly.
    from server import app
    connect_to_db(app)
    print "Connected to DB."

    # In case tables haven't been created, create them.
    db.create_all()
    print "Created tables."
