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
    def read(cls, channel_id):
        """Given a channel id, queries database for active game and returns game
        object if available."""

        return cls.query.filter(cls.channel_id == channel_id, cls.active.is_(True)).first()

    def format_board(self):
        """Takes board stored as JSON string and formats it for display in chat."""

        board = json.loads(self.board)
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

    def display_board(self, response_type):
        formatted_board = self.format_board()
        response = {
            "response_type": response_type,
            "text": "It's <@{}>'s turn!\n```{}```".format(self.active_player, formatted_board)
            }
        return response


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ttt'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

################################################################################

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."

    # In case tables haven't been created, create them.
    db.create_all()
    print "Created tables."
