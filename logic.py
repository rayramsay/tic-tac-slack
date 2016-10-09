import os
from slackclient import SlackClient
from model import Channel

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

    def execute(self):
        """Responds appropriately to text attribute."""

        #Split text string into list of words.
        texts = self.text.split()

        if texts[0] == "play":

            # The word "play" should be followed by a user's @.
            if len(texts) != 2:
                return self.responses["help"]

            elif texts[1].startswith("@"):

                # Verify that the @'d user is on the team.
                player2 = texts[1][1:]
                player2_id = find_id_by_name(player2)

                if not player2_id:
                    # TODO: Add pensive emoji to response.
                    response = {
                        "response_type": "ephemeral",
                        "text": "I don't think {} is on this team.".format(player2)
                    }
                    return response

                # Since player 2 is on the team, check that there's not already
                # a game in this channel.

                channel = Channel.read(self.channel_id)

                # If this channel is not yet in the database, add it.
                if not channel:
                    Channel.create(self.channel_id)

                # If this channel does not have an active game, create one and update channel.
                elif not channel.game_id:
                    pass

            else:
                response = self.responses["help"]

        else:
            response = self.responses["help"]

        return response
