from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Channel(db.Model):
    """Channel object to keep track of whether there's an active game in this channel."""

    __tablename__ = "channels"

    channel_id = db.Column(db.String(64), primary_key=True)
    game_id = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        """Provide a human-readable representation of an instance of a channel."""

        return "<Channel channel_id=%s game_id=%s>" % (self.channel_id, self.game_id)

    @classmethod
    def read(cls, channel_id):
        """Given channel id, queries database for record and returns channel object if
        available."""

        return cls.query.filter(cls.channel_id == channel_id).first()

    @classmethod
    def create(cls, channel_id):
        """Given channel id, adds new channel to the database."""

        channel = cls(channel_id=channel_id)
        db.session.add(channel)
        db.session.commit()


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
