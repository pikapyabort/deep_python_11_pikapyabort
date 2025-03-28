import unittest
from unittest import mock
from predict_message import predict_message_mood


class TestPredictMessageMood(unittest.TestCase):

    def test_real_model_prediction(self):
        message = "TesT"
        result = predict_message_mood(message)
        assert result == "норм"

    @mock.patch("predict_message.SomeModel.predict")
    def test_predict_called_with_proper_string(self, mock_predict):
        message = "test"
        mock_predict.return_value = 0.5
        predict_message_mood(message)
        mock_predict.assert_called_once_with(message)

    @mock.patch("predict_message.SomeModel.predict")
    def test_bad_threshold(self, mock_predict):
        mock_predict.return_value = 0.2
        self.assertEqual(predict_message_mood("test"), "неуд")
        mock_predict.assert_called_once_with("test")

    @mock.patch("predict_message.SomeModel.predict")
    def test_good_thresold(self, mock_predict):
        mock_predict.return_value = 0.9
        self.assertEqual(predict_message_mood("test"), "отл")
        mock_predict.assert_called_once_with("test")

    @mock.patch("predict_message.SomeModel.predict")
    def test_normal_threshold(self, mock_predict):
        mock_predict.return_value = 0.5
        self.assertEqual(predict_message_mood("test"), "норм")
        mock_predict.assert_called_once_with("test")

    @mock.patch("predict_message.SomeModel.predict")
    def test_custom_thresholds(self, mock_predict):
        mock_predict.return_value = 0.85
        self.assertEqual(predict_message_mood("test", 0.8, 0.99), "норм")
        mock_predict.assert_called_once_with("test")

    @mock.patch("predict_message.SomeModel.predict")
    def test_bad_threshold_boundary_equal(self, mock_predict):
        mock_predict.return_value = 0.3
        self.assertEqual(predict_message_mood("test"), "норм")
        mock_predict.assert_called_once_with("test")

    @mock.patch("predict_message.SomeModel.predict")
    def test_bad_threshold_boundary_just_under(self, mock_predict):
        mock_predict.return_value = 0.2999
        self.assertEqual(predict_message_mood("test"), "неуд")
        mock_predict.assert_called_once_with("test")

    @mock.patch("predict_message.SomeModel.predict")
    def test_bad_threshold_boundary_just_over(self, mock_predict):
        mock_predict.return_value = 0.3001
        self.assertEqual(predict_message_mood("test"), "норм")
        mock_predict.assert_called_once_with("test")

    @mock.patch("predict_message.SomeModel.predict")
    def test_good_threshold_boundary_equal(self, mock_predict):
        mock_predict.return_value = 0.8
        self.assertEqual(predict_message_mood("test"), "норм")
        mock_predict.assert_called_once_with("test")

    @mock.patch("predict_message.SomeModel.predict")
    def test_good_threshold_boundary_just_under(self, mock_predict):
        mock_predict.return_value = 0.7999
        self.assertEqual(predict_message_mood("test"), "норм")
        mock_predict.assert_called_once_with("test")

    @mock.patch("predict_message.SomeModel.predict")
    def test_good_threshold_boundary_just_over(self, mock_predict):
        mock_predict.return_value = 0.8001
        self.assertEqual(predict_message_mood("test"), "отл")
        mock_predict.assert_called_once_with("test")

    @mock.patch("predict_message.SomeModel.predict")
    def test_good_mood_upper_limit(self, mock_predict):
        mock_predict.return_value = 1.0
        self.assertEqual(predict_message_mood("test"), "отл")
        mock_predict.assert_called_once_with("test")

    @mock.patch("predict_message.SomeModel.predict")
    def test_bad_mood_lower_limit(self, mock_predict):
        mock_predict.return_value = 0.0
        self.assertEqual(predict_message_mood("test"), "неуд")
        mock_predict.assert_called_once_with("test")

    @mock.patch("predict_message.SomeModel.predict")
    def test_custom_threshold_just_under_good(self, mock_predict):
        mock_predict.return_value = 0.599
        self.assertEqual(predict_message_mood("test", 0.3, 0.6), "норм")
        mock_predict.assert_called_once_with("test")

    @mock.patch("predict_message.SomeModel.predict")
    def test_custom_threshold_exact_good(self, mock_predict):
        mock_predict.return_value = 0.6
        self.assertEqual(predict_message_mood("test", 0.3, 0.6), "норм")
        mock_predict.assert_called_once_with("test")

    @mock.patch("predict_message.SomeModel.predict")
    def test_custom_threshold_just_over_good(self, mock_predict):
        mock_predict.return_value = 0.601
        self.assertEqual(predict_message_mood("test", 0.3, 0.6), "отл")
        mock_predict.assert_called_once_with("test")
