import os
from slackclient import SlackClient
from model import Channel, Game

# Remember to ``source secrets.sh``!
COMMAND_TOKEN = os.environ['COMMAND_TOKEN']
API_TOKEN = os.environ['API_TOKEN']
SLACK_CLIENT = SlackClient(API_TOKEN)


def find_id_by_name(name):
    """Searches team members for name. Returns id if available."""
    users_call = SLACK_CLIENT.api_call("users.list")
    if users_call.get("ok"):
        for member in users_call["members"]:
            if member["name"] == name:
                return member["id"]


class Command(object):

    responses = {
        "help": {
            "response_type": "ephemeral",  # Only displays to that user.
            "text": "To start a game, type `/ttt play @[username]`. \
To see the current board and whose turn it is, type `/ttt board`. \
If it's your turn, type `/ttt move [square].`\n \
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
            "text": "I'm sorry, there's already a game in this channel. \
Each channel can only host one game at a time. Type `/ttt board` to see the game in progress."
        },
        "no_player2": {
            "response_type": "ephemeral",
            "text": "I'm sorry, the person you want to play isn't on this team. \
Please make sure you spelled their username correctly."
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

    def token_is_valid(self):
        """Validates the token by comparing it to global variable COMMAND_TOKEN."""
        return self.token == COMMAND_TOKEN

    def play(self, texts):
        """Actions to take if texts[0] is `play`."""

        # The word "play" should be followed by @username only.
        if len(texts) != 2:
            return self.responses["help"]

        elif texts[1].startswith("@"):

            # Verify that the @'d user is on the team.
            player2 = texts[1][1:]
            player2_id = find_id_by_name(player2)
            if not player2_id:
                return self.responses["no_player2"]

            channel = Channel.read(self.channel_id)

            # If this channel is not yet in the database, add it.
            if not channel:
                Channel.create(self.channel_id)

            else:
                # Check that there's not already a game in this channel.
                if channel.game_id:
                    return self.responses["game_already"]

               # Since this channel does not have an active game, create one.
                Game.create(self.channel_id, self.user_id, player2_id)
                game = Game.read_by_channel(self.channel_id)

                formatted_board = game.format_board()
                response = {
                    "response_type": "ephemeral",
                    "text": "{}".format(formatted_board)
                    }
                return response

    def execute(self):
        """Responds appropriately to text attribute."""

        if not self.text:
            return self.responses["help"]

        #Split text string into list of words.
        texts = self.text.split()

        if texts[0] == "play":
            self.play(texts)

        else:
            return self.responses["help"]
