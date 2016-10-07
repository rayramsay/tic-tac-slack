import os

# Remember to ``source secrets.sh``!
SLACK_TOKEN = os.environ['SLACK_TOKEN']


class Command(object):

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
        """Validates the token by comparing it to global variable SLACK_TOKEN."""
        return self.token == SLACK_TOKEN

    def execute(self):
        """Responds appropriately to text attribute."""

        if (not self.text
                or self.text == 'help'
                or self.text not in ['play', 'board', 'move']):

            response = {
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

        return response
