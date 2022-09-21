import unittest
import json
from unittest.mock import patch
from faker import Faker
import json_parser
from json_parser import parse_json


class TestParsingJson(unittest.TestCase):
    """
    This class tests parse_json function from json_parser
    """
    def setUp(self):
        fake = Faker()
        user_dict = {
            "name": fake.first_name(),
            "surname": fake.last_name(),
            "country": fake.country(),
            "sentence": fake.sentence(nb_words=4, ext_word_list=['first', 'second', 'third', 'fourth']),
            "town": "Kovrov"
        }
        self.json_str = json.dumps(user_dict)

    @patch("json_parser.keyword_handler")
    def test_parsing_json(self, keyword_handler_mock):
        keyword_handler_mock.return_value = None

        parse_json(self.json_str, ["name", "surname", "town", "sentence", "something"],
                   ["Somebody_", "Kovrov"],
                   json_parser.keyword_handler)

        self.assertTrue(keyword_handler_mock.called)
        self.assertEqual(
            [unittest.mock.call("Kovrov")],
            keyword_handler_mock.mock_calls
        )


if __name__ == '__main__':
    unittest.main()
