from process_json import process_json


def test_empty_required_keys_and_tokens():
    json_str = '{"key1": "Word1 word2"}'
    required_keys = []
    tokens = []
    results = []
    process_json(
        json_str,
        required_keys,
        tokens,
        lambda x, y: results.append((x, y)))
    assert not results


def test_empty_json():
    json_str = '{}'
    required_keys = ["key1"]
    tokens = ["token1"]
    results = []
    process_json(
        json_str,
        required_keys,
        tokens,
        lambda x, y: results.append((x, y)))
    assert not results


def test_no_matching_keys():
    json_str = '{"key1": "Word1 word2"}'
    required_keys = ["key2"]
    tokens = ["word1", "word2"]
    results = []
    process_json(
        json_str,
        required_keys,
        tokens,
        lambda x, y: results.append((x, y)))
    assert not results


def test_no_token_in_value():
    json_str = '{"key1": "Just some text"}'
    required_keys = ["key1"]
    tokens = ["word1", "word2"]
    results = []
    process_json(
        json_str,
        required_keys,
        tokens,
        lambda x, y: results.append((x, y)))
    assert not results


def test_key_case_sensitivity():
    json_str = '{"key1": "Word1 word2", "Key2": "word2 word3"}'
    required_keys = ["Key1", "key2"]
    tokens = ["word1", "word2", "word3"]
    results = []
    process_json(
        json_str,
        required_keys,
        tokens,
        lambda x, y: results.append((x, y)))
    assert not results


def test_token_case_insensitivity():
    json_str = '{"key1": "Word1 word2"}'
    required_keys = ["key1"]
    tokens = ["wOrD1", "WORD2"]
    results = []
    process_json(
        json_str,
        required_keys,
        tokens,
        lambda x, y: results.append((x, y)))
    assert results == [("key1", "wOrD1"), ("key1", "WORD2")]


def test_multiple_keys_multiple_tokens():
    json_str = (
        '{"key1": "Word1 word2 word1", '
        '"key2": "word2 word3", '
        '"another_key": "Word1"}'
    )
    required_keys = ["key1", "key2", "ANOTHER_KEY"]
    tokens = ["WORD1", "word2", "WORD5"]
    results = []
    process_json(
        json_str,
        required_keys,
        tokens,
        lambda x, y: results.append((x, y)))
    assert len(results) == 3
    assert results == [("key1", "WORD1"), ("key1", "word2"), ("key2", "word2")]


def test_default_callback(capfd):
    json_str = '{"key1": "Word1 word2"}'
    required_keys = ["key1"]
    tokens = ["word1", "word2"]
    process_json(json_str, required_keys, tokens)
    captured = capfd.readouterr()
    lines = captured.out.strip().split('\n')
    assert lines == [
        'key = "key1", token = "word1"',
        'key = "key1", token = "word2"',
    ]
