from predict_message import predict_message_mood


def test_short_message():
    text = "Вулкан"
    assert predict_message_mood(text) == "неуд"


def test_long_message():
    text = "ЧАПАЕВ И ПУСТОТА"
    assert predict_message_mood(text) == "отл"


def test_custom_thresholds():
    text = "ЧАПАЕВ И ПУСТОТа"
    assert predict_message_mood(text, 0.8, 0.99) == "норм"
