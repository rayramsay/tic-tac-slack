import os
from slackclient import SlackClient
from model import Game

# Remember to `source secrets.sh`!
COMMAND_TOKEN = os.environ['COMMAND_TOKEN']
API_TOKEN = os.environ['API_TOKEN']

slack_client = SlackClient(API_TOKEN)


def find_id_by_name(name):
    """Searches team members for name. Returns id if available."""
    users_call = slack_client.api_call("users.list")
    if users_call.get("ok"):
        for member in users_call["members"]:
            if member["name"].lower() == name:
                return member["id"]


class Command(object):

    responses = {
        "help": {
            "response_type": "ephemeral",
            "text": "To start a game, type `/ttt play @[username]`. \
To see the current board and whose turn it is, type `/ttt board`. \
If it's your turn, type `/ttt move [square]`.\n \
```\
| A1 | A2 | A3 |\n\
|----+----+----|\n\
| B1 | B2 | B3 |\n\
|----+----+----|\n\
| C1 | C2 | C3 |\n\
```\
"
        },
        "game_already": {
            "response_type": "ephemeral",
            "text": "I'm sorry, there's already a game being played in this channel. \
Each channel can only host one game at a time. Type `/ttt board` to see the game in progress."
        },
        "no_game": {
            "response_type": "ephemeral",
            "text": "I'm sorry, there's not currently a game being played in this channel. \
You're welcome to start one! Type `/ttt play @[username]`."
        },
        "no_player2": {
            "response_type": "ephemeral",
            "text": "I'm sorry, the person you want to play with isn't on this team. \
Please check that you spelled their username correctly."
        },
        "not_turn": {
            "response_type": "ephemeral",
            "text": "I'm sorry, it's not your turn. Type `/ttt board` to see whose turn it is."
        }
    }

    def __init__(self, token, team_id, team_domain, channel_id, channel_name, user_id, user_name, command, text, response_url):
        """Instantiates a command."""

        self.token = token
        self.team_id = team_id
        self.team_domain = team_domain
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.user_id = user_id
        self.user_name = user_name
        self.command = command
        self.text = text.lower()
        self.response_url = response_url

    def is_valid(self):
        """Validates the token."""
        return self.token == COMMAND_TOKEN

    def board(self, texts):
        """Displays the board (if available) to the user."""

        game = Game.read(self.channel_id)

        # Check that there is a game to display.
        if not game:
            return self.responses["no_game"]

        return game.display_board("ephemeral")

    def play(self, texts):
        """Starts a new game if appropriate."""

        # `Play` should only be followed by `@[username]`.
        if texts[1].startswith("@"):

            # Check that there's not already a game in this channel.
            if Game.read(self.channel_id):
                return self.responses["game_already"]

            # Verify that the @'d user is on the team.
            player2 = texts[1][1:]
            player2_id = find_id_by_name(player2)
            if not player2_id:
                return self.responses["no_player2"]

           # Since this channel does not have an active game, create one.
            Game.create(self.channel_id, self.user_id, player2_id)
            game = Game.read(self.channel_id)

            return game.display_board("in_channel")

        else:
            return self.responses["help"]

    def move(self, texts):
        """Records move if appropriate."""

        moves = ['a1', 'a2', 'a3', 'b1', 'b2', 'b3', 'c1', 'c2', 'c3']
        game = Game.read(self.channel_id)

        # Check that there's a game to play.
        if not game:
            return self.responses["no_game"]

        # Check that the user is the active player.
        if not self.user_id == game.active_player:
            return self.responses["not_turn"]

        # Check that it's a legal move.
        if texts[1] in moves:
            pass

        else:
            return self.responses["help"]

    def execute(self):
        """Responds appropriately to text attribute."""

        if not self.text:
            return self.responses["help"]

        #Split text string into list of words.
        texts = self.text.split()

        if texts[0] == "play" and len(texts) == 2:
            return self.play(texts)

        elif texts[0] == "move" and len(texts) == 2:
            return self.move(texts)

        # The word `board` should not be followed by anything else.
        elif texts[0] == "board" and len(texts) == 1:
            return self.board(texts)

        else:
            return self.responses["help"]
