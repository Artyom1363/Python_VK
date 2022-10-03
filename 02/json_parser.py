import json


def keyword_handler(keyword):
    print("keyword_handler was called ", f"{keyword=}")


def parse_json(json_str: str, required_fields, keywords,
               keyword_callback=None):
    """

    Args:
        json_str: this is string with json
        required_fields: field in json_str which must be checked
        keywords: words - values of required_fields, which must be found
        keyword_callback: - function, which will be called,
                            when we find keyword. If keyword_callback
                            is None nothing will be done

    Returns:
        None
    """
    if keyword_callback is None:
        return

    if not callable(keyword_callback):
        raise TypeError("keyword_callback must be callable")

    json_obj = json.loads(json_str)
    for field in required_fields:
        if field not in json_obj:
            continue
        words = json_obj[field].split()
        for word in words:
            if word in keywords:
                keyword_callback(word)
