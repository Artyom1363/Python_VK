import unittest
from unittest.mock import patch
import json_parser
from json_parser import parse_json


# def keyword_handler(keyword):
#     print("keyword_handler was called ", f"{keyword=}")


class TestParsingJson(unittest.TestCase):
    @patch("json_parser.keyword_handler")
    def test_parsing_json(self, keyword_handler_mock):
        keyword_handler_mock.return_value = None
        json_str = '{"squadName": "Super hero squad", ' \
                   '"homeTown": "Metro City", ' \
                   '"formed": 2016, "secretBase": "Super tower", ' \
                   '"active": true}'

        parse_json(json_str, ["squadName", 'test'], ["hero", 'make'], json_parser.keyword_handler)
        self.assertTrue(keyword_handler_mock.called)
        self.assertEqual(
            [unittest.mock.call('hero')],
            keyword_handler_mock.mock_calls
        )
        print(keyword_handler_mock.mock_calls)
        # print(keyword_handler_mock.called)


if __name__ == '__main__':
    unittest.main()
