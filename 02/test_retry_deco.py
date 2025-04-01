import pytest
from retry_deco import retry_deco


def test_add_positional_args(capfd):

    @retry_deco(3)
    def add(a, b):
        return a + b

    add(4, 2)
    captured = capfd.readouterr()
    lines = captured.out.strip().split("\n")
    assert len(lines) == 1
    assert (
        'run "add" with positional args = (4, 2), '
        'keyword kwargs = {}, '
        'attempt = 1, result = 6'
    ) in lines[0]


def test_add_mixed_args(capfd):

    @retry_deco(3)
    def add(a, b):
        return a + b

    add(4, b=3)
    captured = capfd.readouterr()
    lines = captured.out.strip().split("\n")
    assert len(lines) == 1
    assert (
        'run "add" with positional args = (4,), '
        'keyword kwargs = {\'b\': 3}, '
        'attempt = 1, result = 7'
    ) in lines[0]


def test_check_str_success_true(capfd):

    @retry_deco(3)
    def check_str(value=None):
        return isinstance(value, str)

    result = check_str(value="123")
    captured = capfd.readouterr()
    lines = captured.out.strip().split("\n")
    assert len(lines) == 1
    assert (
        'run "check_str" with positional args = (), '
        'keyword kwargs = {\'value\': \'123\'}, '
        'attempt = 1, result = True'
    ) in lines[0]
    assert result is True


def test_check_str_success_false(capfd):

    @retry_deco(3)
    def check_str(value=None):
        return isinstance(value, str)

    result = check_str(value=1)
    captured = capfd.readouterr()
    lines = captured.out.strip().split("\n")
    assert len(lines) == 1
    assert (
        'run "check_str" with positional args = (), '
        'keyword kwargs = {\'value\': 1}, '
        'attempt = 1, result = False'
    ) in lines[0]
    assert result is False


def test_check_str_retry_3_attempts(capfd):

    @retry_deco(3)
    def check_str(value=None):
        if value is None:
            raise ValueError("value is None!")

    with pytest.raises(ValueError):
        check_str(value=None)
    captured = capfd.readouterr()
    lines = captured.out.strip().split("\n")
    assert len(lines) == 3
    for i, line in enumerate(lines, start=1):
        assert f'attempt = {i}, exception = ValueError' in line


def test_check_int_success(capfd):

    @retry_deco(2, (ValueError,))
    def check_int(value=None):
        return isinstance(value, int)

    result = check_int(value=1)
    captured = capfd.readouterr()
    lines = captured.out.strip().split("\n")
    assert len(lines) == 1
    assert (
        'run "check_int" with positional args = (), '
        'keyword kwargs = {\'value\': 1}, '
        'attempt = 1, result = True'
    ) in lines[0]
    assert result is True


def test_check_int_expected_exception(capfd):

    @retry_deco(2, (ValueError,))
    def check_int(value=None):
        if value is None:
            raise ValueError("value is None!")

    with pytest.raises(ValueError):
        check_int(value=None)
    captured = capfd.readouterr()
    lines = captured.out.strip().split("\n")
    assert len(lines) == 1
    assert 'attempt = 1, exception = ValueError' in lines[0]


def test_no_retries(capfd):

    @retry_deco(0)
    def fail_once():
        raise RuntimeError("Error")

    with pytest.raises(RuntimeError):
        fail_once()
    captured = capfd.readouterr()
    lines = captured.out.strip().split("\n")
    assert len(lines) == 1
    assert "attempt = 1, exception = RuntimeError" in lines[0]


def test_retry_success_after_failure(capfd):
    call_count = 0

    @retry_deco(3)
    def sometimes_fail():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            raise RuntimeError("Error")
        return "OK"

    result = sometimes_fail()
    assert result == "OK"
    captured = capfd.readouterr()
    lines = captured.out.strip().split("\n")
    assert len(lines) == 2
    assert "attempt = 1, exception = RuntimeError" in lines[0]
    assert "attempt = 2, result = OK" in lines[1]
