import unittest
from unittest.mock import patch
import json_parser
import json
from json_parser import parse_json
from faker import Faker


class TestParsingJson(unittest.TestCase):

    def setUp(self):
        fake = Faker()
        user_dict = {
            "name": fake.first_name(),
            "surname": fake.last_name(),
            "country": fake.country(),
            "town": "Kovrov"
        }
        self.json_str = json.dumps(user_dict)

    @patch("json_parser.keyword_handler")
    def test_parsing_json(self, keyword_handler_mock):
        keyword_handler_mock.return_value = None

        parse_json(self.json_str, ["name", "surname", "town"], ["Larisa_", "Kovrov"], json_parser.keyword_handler)
        self.assertTrue(keyword_handler_mock.called)
        self.assertEqual(
            [unittest.mock.call("Kovrov")],
            keyword_handler_mock.mock_calls
        )


if __name__ == '__main__':
    unittest.main()
