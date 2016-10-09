from flask import Flask, request, jsonify, abort
from logic import Command
from model import Channel, connect_to_db, db

app = Flask(__name__)


@app.route('/ttt', methods=['POST'])
def parse():
    """Instantiates a command object and responds to it."""

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

    print text

    command = Command(token, team_id, team_domain, channel_id, channel_name, user_id, user_name, command, text, response_url)

    if not command.token_is_valid():
        abort(400)

    response = command.execute()

    return jsonify(response)


################################################################################

if __name__ == "__main__":

    # Set debug = True in order to invoke the DebugToolbarExtension.
    app.debug = True

    # Connect to database.
    connect_to_db(app)

    # Must specify host for Vagrant.
    app.run(host="0.0.0.0")
