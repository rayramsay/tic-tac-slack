import os

from flask import Flask, request, jsonify, abort

app = Flask(__name__)

# Remember to ``source secrets.sh``!
SLACK_TOKEN = os.environ['SLACK_TOKEN']

@app.route('/ttt', methods=['POST'])
def parse():
    """Parse the command parameters, validate them, and respond."""

    token = request.form.get('token', None)
    team_id = request.form.get('team_id', None)
    team_domain = request.form.get('team_domain', None)
    channel_id = request.form.get('channel_id', None)
    channel_name = request.form.get('channel_name', None)
    user_id = request.form.get('user_id', None)
    user_name = request.form.get('user_name', None)
    command = request.form.get('command', None)
    text = request.form.get('text', None)
    response_url = request.form.get('response_url', None)

    # Validate the token.
    if not token or token != SLACK_TOKEN:
        abort(400)

    # Validate the text.
    if text:
        text = text.lower()

    if not text or text == 'help' or text not in ['play', 'board']:
        return jsonify({
            "response_type": "ephemeral",  # Only displays to that user.
            "text": "*How to use /ttt.*",
            "attachments": [{
                "mrkdwn_in": ["text"],
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
                }]
        })


################################################################################

if __name__ == "__main__":

    # Set debug = True in order to invoke the DebugToolbarExtension.
    app.debug = True

    # Use the DebugToolbarExtension.
    # DebugToolbarExtension(app)

    # There's currently a bug in flask 0.11 that prevents template reloading.
    app.jinja_env.auto_reload = True

    # Connect to database.
    #connect_to_db(app)

    # Must specify host for Vagrant.
    app.run(host="0.0.0.0")
