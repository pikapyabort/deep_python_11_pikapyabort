def filter_lines(file_or_path, search_words, stop_words):
    search_set = set(word.lower() for word in search_words)
    stop_set = set(word.lower() for word in stop_words)
    if hasattr(file_or_path, 'read'):
        for line in file_or_path:
            stripped_line = line.strip()
            if not stripped_line:
                continue
            words_in_line = stripped_line.lower().split()
            if search_set.intersection(words_in_line):
                if not stop_set.intersection(words_in_line):
                    yield line.rstrip('\n')
    else:
        with open(file_or_path, 'r', encoding='utf-8') as lines_iter:
            for line in lines_iter:
                stripped_line = line.strip()
                if not stripped_line:
                    continue
                words_in_line = stripped_line.lower().split()
                if search_set.intersection(words_in_line):
                    if not stop_set.intersection(words_in_line):
                        yield line.rstrip('\n')
