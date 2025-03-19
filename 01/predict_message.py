class SomeModel:  # pylint: disable=too-few-public-methods
    def predict(self, message: str) -> float:  # pylint: disable=unused-argument
        return sum(1 for c in message if c.isupper()) / max(1, len(message))


def predict_message_mood(
    message: str,
    bad_thresholds: float = 0.3,
    good_thresholds: float = 0.8,
) -> str:
    model = SomeModel()
    result = model.predict(message)
    if result < bad_thresholds:
        return "неуд"
    if result > good_thresholds:
        return "отл"
    return "норм"
