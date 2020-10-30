import google.cloud.language
import google.cloud
import numpy as np
import os


def average(target_list):
    return sum(target_list) / len(target_list)


class SentimentContainer:
    """ Container which holds magnitude and score of multiple Google Cloud API Sentiment Returns """
    def __init__(self):
        self.magnitude = []
        self.score = []

    def __len__(self):
        return len(self.magnitude)

    def add(self, sentiment):
        self.magnitude.append(sentiment.magnitude)
        self.score.append(sentiment.score)

    def calculate(self):
        mean_magnitude = np.mean(self.magnitude)
        mean_score = np.mean(self.score)
        return {"magnitude": mean_magnitude, "score": mean_score}
    
    def get_magnitude(self):
        return np.mean(self.magnitude)
    
    def get_score(self):
        return np.mean(self.score)


class SentimentAnalyzer(object):
    """ Class to interact with Google Cloud NLP Sentiment Analysis API """
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = self.load_cloud_nlp_config()
        self.client = google.cloud.language.LanguageServiceClient()

    def load_cloud_nlp_config(self):
        """ 
        Helper function to load Google Cloud NLP config file. Sets environment variable
        GOOGLE_APPLICATION_CREDENTIALS given the service account key from the Cloud NLP json.

        :param config_file: String containing path to config file
        """
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.config_file
        return

    def analyze_text(self, text):
        """
        Function that calls Google Cloud NLP API for given text to analyze sentiment

        :param text: String containing text to be analyzed
        """
        document = google.cloud.language.types.Document(content=text,
                type=google.cloud.language.enums.Document.Type.PLAIN_TEXT)
        sentiment = self.client.analyze_sentiment(document=document).document_sentiment
        return sentiment
    
    def analyze_entities(self, text):
        """
        Function that calls Google Cloud NLP API for given text to get entities in text

        :param text: String containing text to be analyzed
        """
        document = google.cloud.language.types.Document(content=text,
                type=google.cloud.language.enums.Document.Type.PLAIN_TEXT)
        sentiment = self.client.analyze_entity_sentiment(document=document)
        return sentiment

    @staticmethod
    def get_semantic_sentiment(sentiment):
        """
        Helper function to return semantically meaningful sentiment analysis.

        :param sentiment: Dictionary with keys "score" and "magnitude" containting float values

        :return: String containing semantically meaning analysis of sentiment
        """
        score_thresh = 0.10

        if sentiment["score"] >= score_thresh:
            if sentiment["magnitude"] > 0.15:
                semantic_sentiment = "Clearly Positive"
            else:
                semantic_sentiment = "Positive"
        elif sentiment["score"] <= -score_thresh:
            if sentiment["magnitude"] > 0.15:
                semantic_sentiment = "Clearly Negative"
            else:
                semantic_sentiment = "Negative"
        elif (sentiment["score"] > -score_thresh and sentiment["score"] < score_thresh) and sentiment["magnitude"] > 0.15:
            semantic_sentiment = "Mixed"
        else:
            semantic_sentiment = "Neutral"
        return semantic_sentiment

    @staticmethod
    def filter_strings(strings, keywords):
        """ 
        Helper function that searches a list of strings for keyworkds located in a list of keywords, then returns the
        strings that contain the keyword. Note that this search is NOT case sensitive.

        :param strings: List of strings to be searched :param keywords: List of keywords to search for

        :return: List of strings which contained one or more of the keywords 
        """

        key_strings = [x for x in strings if any(y.lower() in x.lower() for y in keywords)]
        return key_strings


