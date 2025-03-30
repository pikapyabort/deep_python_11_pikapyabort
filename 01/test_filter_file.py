import io
from filter_file import filter_lines


def test_basic_filtering():
    text_data = """ a Роза упала на лапу Азора

Роз
Привет мир
Роза
розан
"""
    file_like = io.StringIO(text_data)
    search_words = ["роза"]
    stop_words = ["азора"]
    result = list(filter_lines(file_like, search_words, stop_words))
    assert result == ["Роза"]


def test_multiple_search_words():
    text_data = """foo bar
bar foo
foo foo
"""
    file_like = io.StringIO(text_data)
    search_words = ["foo", "bar"]
    stop_words = []
    result = list(filter_lines(file_like, search_words, stop_words))
    assert len(result) == 3
    assert result == ["foo bar", "bar foo", "foo foo"]


def test_stop_words_override():
    text_data = """word1 word2 stopword word3
searchword stopword
searchword
"""
    file_like = io.StringIO(text_data)
    search_words = ["searchword", "word1"]
    stop_words = ["stopword"]
    result = list(filter_lines(file_like, search_words, stop_words))
    assert result == ["searchword"]


def test_file_path(tmp_path):
    test_file = tmp_path / "test_data.txt"
    test_file.write_text(
        "a Роза упала на лапу Азора\n"
        "\n"
        "Роз\n"
        "Привет мир\n"
        "Роза\n"
        "розан\n",
        encoding="utf-8"
    )
    search_words = ["роза"]
    stop_words = ["азора"]
    results = list(filter_lines(str(test_file), search_words, stop_words))
    assert results == ["Роза"]


def test_single_char_search_stop():
    text_data = """u c
u f c
U c
U F c
ufc
"""
    file_like = io.StringIO(text_data)
    search_words = ["u"]
    stop_words = ["f"]
    results = list(filter_lines(file_like, search_words, stop_words))
    assert results == ["u c", "U c"]


def test_no_search_words():
    text_data = """u f c
U F C
ufc
"""
    file_like = io.StringIO(text_data)
    search_words = []
    stop_words = ["ufc"]
    results = list(filter_lines(file_like, search_words, stop_words))
    assert not results
