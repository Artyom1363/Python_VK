import json


def keyword_handler(keyword):
    print("keyword_handler was called ", f"{keyword=}")


def parse_json(json_str: str, required_fields, keywords, keyword_callback):
    """

    Args:
        json_str: this is string with json
        required_fields: field in json_str which must be checked
        keywords: words - values of required_fields, which must be found
        keyword_callback: - function, which will be called, when we find keyword

    Returns:
        None
    """
    json_obj = json.loads(json_str)
    for field in required_fields:
        if field not in json_obj:
            continue
        words = json_obj[field].split()
        for word in words:
            if word in keywords:
                keyword_callback(word)
