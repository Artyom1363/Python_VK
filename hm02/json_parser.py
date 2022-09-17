import json


def keyword_handler(keyword):
    print("keyword_handler was called ", f"{keyword=}")


def parse_json(json_str: str, required_fields, keywords, keyword_callback):
    json_obj = json.loads(json_str)
    for field in required_fields:
        if field not in json_obj:
            continue
        words = json_obj[field].split()
        for word in words:
            if word in keywords:
                keyword_callback(word)
