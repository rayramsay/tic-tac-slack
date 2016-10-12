import unittest
import server
import model


class TokenTest(unittest.TestCase):

    def setUp(self):
        model.connect_to_db(server.app, "postgresql:///testdb")
        self.client = server.app.test_client()
        server.app.config['TESTING'] = True
        model.db.create_all()

    def tearDown(self):
        model.db.session.close()
        model.db.drop_all()

    def test_bad_token(self):
        payload = {
            "token": "aaa"
        }
        result = self.client.post('/ttt', data=payload)
        self.assertEqual(result.status_code, 400)

    def test_good_token(self):
        payload = {
            "token": "h5o2iRGZMlaCEIA0tKPdi3SY"
        }
        result = self.client.post('/ttt', data=payload)
        self.assertEqual(result.status_code, 200)


class HelpTest(unittest.TestCase):

    def setUp(self):
        # Connect to test database
        model.connect_to_db(server.app, "postgresql:///testdb")

        self.client = server.app.test_client()
        server.app.config['TESTING'] = True

        # Create tables and add sample data
        model.db.create_all()
        # model.example_data()

    def tearDown(self):
        model.db.session.close()
        model.db.drop_all()

    def test_blank_text(self):
        """`/ttt` without any text should trigger help."""

        payload = {
            "token": "h5o2iRGZMlaCEIA0tKPdi3SY",
            "command": "/ttt",
            "text": ""
        }
        result = self.client.post('/ttt', data=payload)
        self.assertIn('A1', result.data)

    def test_help(self):
        payload = {
            "token": "h5o2iRGZMlaCEIA0tKPdi3SY",
            "command": "/ttt",
            "text": "help"
        }
        result = self.client.post('/ttt', data=payload)
        self.assertIn('A1', result.data)

    def test_short_move(self):
        """`move` without any additional words should trigger help."""
        payload = {
            "token": "h5o2iRGZMlaCEIA0tKPdi3SY",
            "channel_id": "C2LD6AS75",
            "user_id": "U2KTWAQ6M",
            "user_name": "oxo",
            "command": "/ttt",
            "text": "move"
        }
        result = self.client.post('/ttt', data=payload)
        self.assertIn('A1', result.data)

    def test_short_play(self):
        """`play` without any additional words should trigger help."""
        payload = {
            "token": "h5o2iRGZMlaCEIA0tKPdi3SY",
            "channel_id": "C2LD6AS75",
            "user_id": "U2KTWAQ6M",
            "user_name": "oxo",
            "command": "/ttt",
            "text": "play"
        }
        result = self.client.post('/ttt', data=payload)
        self.assertIn('A1', result.data)

    def test_play_no_at(self):
        """`play` without an @ should trigger help."""
        payload = {
            "token": "h5o2iRGZMlaCEIA0tKPdi3SY",
            "channel_id": "C2LD6AS75",
            "user_id": "U2KTWAQ6M",
            "user_name": "oxo",
            "command": "/ttt",
            "text": "play xox"
        }
        result = self.client.post('/ttt', data=payload)
        self.assertIn('A1', result.data)


class NoGameTest(unittest.TestCase):

    def setUp(self):
        # Connect to test database
        model.connect_to_db(server.app, "postgresql:///testdb")

        self.client = server.app.test_client()
        server.app.config['TESTING'] = True

        # Create tables and add sample data
        model.db.create_all(app=server.app)

        # model.example_data()

    def tearDown(self):
        model.db.session.close()
        model.db.drop_all()

    def test_board_no_game(self):
        """Asking to see there board when there's no game in progress should
        trigger no_game response."""

        payload = {
            "token": "h5o2iRGZMlaCEIA0tKPdi3SY",
            "channel_id": "C2LD6AS75",
            "user_id": "U2KTWAQ6M",
            "user_name": "oxo",
            "command": "/ttt",
            "text": "board"
        }
        result = self.client.post('/ttt', data=payload)
        self.assertIn('not currently a game being played', result.data)
        self.assertNotIn('|---+---+---|', result.data)

    def test_move_no_game(self):
        """Trying to make even a valid `move` when there's no game in progress
        should trigger no_game response."""

        payload = {
            "token": "h5o2iRGZMlaCEIA0tKPdi3SY",
            "channel_id": "C2LD6AS75",
            "user_id": "U2KTWAQ6M",
            "user_name": "oxo",
            "command": "/ttt",
            "text": "move a1"
        }
        result = self.client.post('/ttt', data=payload)
        self.assertIn('not currently a game being played', result.data)
        self.assertNotIn('|---+---+---|', result.data)

    def test_resign_no_game(self):
        """Trying to `resign` when there's no game in progress should trigger
        no_game response."""

        payload = {
            "token": "h5o2iRGZMlaCEIA0tKPdi3SY",
            "channel_id": "C2LD6AS75",
            "user_id": "U2KTWAQ6M",
            "user_name": "oxo",
            "command": "/ttt",
            "text": "resign"
        }
        result = self.client.post('/ttt', data=payload)
        self.assertIn('not currently a game being played', result.data)
        self.assertNotIn('|---+---+---|', result.data)


class BadGameTest(unittest.TestCase):

    def setUp(self):
        # Connect to test database
        model.connect_to_db(server.app, "postgresql:///testdb")

        self.client = server.app.test_client()
        server.app.config['TESTING'] = True

        # Create tables and add sample data
        model.db.create_all()
        # model.example_data()

    def tearDown(self):
        model.db.session.close()
        model.db.drop_all()

    def test_start_game(self):
        payload = {
            "token": "h5o2iRGZMlaCEIA0tKPdi3SY",
            "channel_id": "C2LD6AS75",
            "user_id": "U2KTWAQ6M",
            "user_name": "oxo",
            "command": "/ttt",
            "text": "play @xox"
        }
        result = self.client.post('/ttt', data=payload)
        self.assertIn('turn', result.data)
        self.assertIn('|---+---+---|', result.data)

if __name__ == "__main__":
    unittest.main()
