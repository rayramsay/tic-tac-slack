import unittest
import server
import model


class GameUnitTestCase(unittest.TestCase):

    def setUp(self):
        # Connect to test database
        model.connect_to_db(server.app, "postgresql:///testdb")

        self.client = server.app.test_client()
        server.app.config['TESTING'] = True

        # Create tables and add sample data
        model.db.create_all()
        # model.example_data()

    # def tearDown(self):
    #     model.db.session.close()
    #     model.db.drop_all()

    def start_game(self):

        payload = {
            "token": "h5o2iRGZMlaCEIA0tKPdi3SY",
            "team_id": "T0001",
            "team_domain": "example",
            "channel_id": "C2LD6AS75",
            "channel_name": "test",
            "user_id": "U2KTWAQ6M",
            "user_name": "oxo",
            "command": "/ttt",
            "text": "play @xox",
            "response_url": "https://hooks.slack.com/commands/1234/5678"
        }

        result = self.client.post('/ttt', data=payload)
        self.assertIn('|---+---+---|', result.data)

    def test2(self):
        pass

if __name__ == "__main__":
    unittest.main()
