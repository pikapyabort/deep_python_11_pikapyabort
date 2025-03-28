def _filter_lines_iter(lines_iter, search_set, stop_set):
    for line in lines_iter:
        stripped_line = line.strip()
        if not stripped_line:
            continue
        words_in_line = stripped_line.lower().split()
        if search_set.intersection(words_in_line):
            if not stop_set.intersection(words_in_line):
                yield line.rstrip('\n')


def filter_lines(file_or_path, search_words, stop_words):
    search_set = set(word.lower() for word in search_words)
    stop_set = set(word.lower() for word in stop_words)
    if hasattr(file_or_path, 'read'):
        yield from _filter_lines_iter(file_or_path, search_set, stop_set)
    else:
        with open(file_or_path, 'r', encoding='utf-8') as f:
            yield from _filter_lines_iter(f, search_set, stop_set)
