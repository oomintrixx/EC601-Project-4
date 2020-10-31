from cloud_nlp.sentiment_analysis import SentimentContainer, SentimentAnalyzer
import google
import pytest


class FakeSentiment(object):
    def __init__(self, magnitude, score):
        self.magnitude = magnitude
        self.score = score


class TestGoogleNLPAPIBase(object):
    t = SentimentAnalyzer("cloud_natural_language_api.json")


class TestSentimentContainer:
    def test_add(self):
        s = SentimentContainer()
        f = FakeSentiment(0, 0)
        s.add(f)
        assert s.magnitude == [0]
        assert s.score == [0]

    def test_calculate(self):
        s = SentimentContainer()
        s.add(FakeSentiment(0, 0))
        s.add(FakeSentiment(1, 1))
        s.add(FakeSentiment(2, 2))
        s.add(FakeSentiment(3, 3))
        assert s.calculate() == {"magnitude": 1.5, "score": 1.5}

    def test_len(self):
        s = SentimentContainer()
        s.add(FakeSentiment(0, 0))
        s.add(FakeSentiment(1, 1))
        s.add(FakeSentiment(2, 2))
        s.add(FakeSentiment(3, 3))
        assert len(s) == 4

    def add_junk(self):
        s = SentimentContainer()
        
        with pytest.raises(AttributeError):
            s.add("abc")

        with pytest.raises(AttributeError):
            s.add(0.0)

    def test_magnitude(self):
        s = SentimentContainer()
        s.add(FakeSentiment(0, 0))
        s.add(FakeSentiment(2, 2))
        s.add(FakeSentiment(4, 4))
        s.add(FakeSentiment(6, 6))
        assert s.get_magnitude() == 3.0
    
    def test_score(self):
        s = SentimentContainer()
        s.add(FakeSentiment(0, 0))
        s.add(FakeSentiment(2, 2))
        s.add(FakeSentiment(4, 4))
        s.add(FakeSentiment(6, 6))
        assert s.get_score() == 3.0


class TestConfigLoading:
    def test_empty_config(self):
        config_file = "tests/config_nlp_empty.json"
        with pytest.raises(google.auth.exceptions.DefaultCredentialsError):
            SentimentAnalyzer(config_file)

    def test_empty_key_config(self):
        config_file = "tests/config_nlp_empty_2.json"
        with pytest.raises(google.auth.exceptions.DefaultCredentialsError):
            SentimentAnalyzer(config_file)


class TestSentimentAnalyzer(TestGoogleNLPAPIBase):
    def test_analyze_text_positive(self):
        pos_text = "That was awesome!"
        pass

    def test_analyze_text_negative(self):
        neg_text = "That was horrible."
        pass

    def test_analyze_text_neutral(self):
        neutral_text = "That was okay."
        pass

    def test_analyze_entities_positive(self):
        pos_text = "Joe is great!"
        pass

    def test_analyze_entities_negative(self):
        neg_text = "Joe is a bad person."
        pass

    def test_analyze_entities_neutral(self):
        neg_text = "Joe is okay."
        pass
