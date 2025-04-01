def retry_deco(
    retries: int = 1,
    expected_exceptions: tuple[type[BaseException], ...] | None = None
):
    if expected_exceptions is None:
        expected_exceptions = ()

    def inner_deco(func):
        def inner(*args, **kwargs):
            attempt = 0
            while True:
                attempt += 1
                try:
                    result = func(*args, **kwargs)
                    print(
                        f'run "{func.__name__}" '
                        f"with positional args = {args}, "
                        f"keyword kwargs = {kwargs}, "
                        f"attempt = {attempt}, result = {result}"
                    )
                    return result
                except expected_exceptions as e:
                    print(
                        f'run "{func.__name__}" '
                        f"with positional args = {args}, "
                        f"keyword kwargs = {kwargs}, "
                        f"attempt = {attempt}, exception = {type(e).__name__}"
                    )
                    raise
                except Exception as e:
                    print(
                        f'run "{func.__name__}" '
                        f"with positional args = {args}, "
                        f"keyword kwargs = {kwargs}, "
                        f"attempt = {attempt}, exception = {type(e).__name__}"
                    )
                    if attempt < retries:
                        continue
                    raise
        return inner
    return inner_deco
