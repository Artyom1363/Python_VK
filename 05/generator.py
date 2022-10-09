def gen_from_file(file_obj, words_to_search=None):
    if words_to_search is None:
        words_to_search = []
    with open(file_obj, "r", encoding="utf-8") as file:
        for line in file:
            for word in words_to_search:
                words_in_line = [word_in_line.strip()
                                 for word_in_line in line.lower().split()]
                if word.lower() in words_in_line:
                    yield line
