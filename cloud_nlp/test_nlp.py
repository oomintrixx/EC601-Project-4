from cloud_nlp.sentiment_analysis import SentimentContainer, SentimentAnalyzer
import google
import pytest


class FakeSentiment(object):
    def __init__(self, magnitude, score):
        self.magnitude = magnitude
        self.score = score


class TestGoogleNLPAPIBase(object):
    t = SentimentAnalyzer("cloud_natural_language_api.json")

    @staticmethod
    def convert_sentiment_to_dict(s):
        return {"score": s.score, "magnitude": s.magnitude}

    @staticmethod
    def convert_entity_sentiment_to_dict(s):
        if len(s.entities) > 1:
            raise RuntimeError("Too many entities returned by NLP API!")
        return {"score": s.entities[0].sentiment.score, "magnitude": s.entities[0].sentiment.magnitude}


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
        sentiment = self.convert_sentiment_to_dict(self.t.analyze_text(pos_text))
        assert self.t.get_semantic_sentiment(sentiment) == "Clearly Positive" or self.t.get_semantic_sentiment == "Positive"

    def test_analyze_text_negative(self):
        neg_text = "That was horrible."
        sentiment = self.convert_sentiment_to_dict(self.t.analyze_text(neg_text))
        assert self.t.get_semantic_sentiment(sentiment) == "Clearly Negative" or self.t.get_semantic_sentiment == "Negative"

    def test_analyze_text_neutral(self):
        neutral_text = ""
        sentiment = self.convert_sentiment_to_dict(self.t.analyze_text(neutral_text))
        assert self.t.get_semantic_sentiment(sentiment) == "Neutral"

    def test_analyze_entities_positive(self):
        pos_text = "Joe is great!"
        sentiment = self.convert_entity_sentiment_to_dict(self.t.analyze_entities(pos_text))
        assert self.t.get_semantic_sentiment(sentiment) == "Clearly Positive" or self.t.get_semantic_sentiment == "Positive"

    def test_analyze_entities_negative(self):
        neg_text = "Joe is a bad person."
        sentiment = self.convert_entity_sentiment_to_dict(self.t.analyze_entities(neg_text))
        assert self.t.get_semantic_sentiment(sentiment) == "Clearly Negative" or self.t.get_semantic_sentiment == "Negative"

    def test_analyze_entities_neutral(self):
        neutral_text = "Joe"
        sentiment = self.convert_entity_sentiment_to_dict(self.t.analyze_entities(neutral_text))
        assert self.t.get_semantic_sentiment(sentiment) == "Neutral"

