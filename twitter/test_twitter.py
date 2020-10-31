from twitter.tweets import Tweets
import tweepy
import pytest
import os


class TestTwitterAPIBase:
    t = Tweets("config_private.ini")

class TestConfigLoading:
    """ Tests config file loading  """
    def test_empty_config(self):
        config_file = "tests/config_empty.ini"
        with pytest.raises(KeyError):
            Tweets(config_file)

    def test_empty_key_config(self):
        config_file = "tests/config_empty_2.ini"
        with pytest.raises(RuntimeError):
            Tweets(config_file)

    def test_default_config(self):
        config_file = "config.ini"
        with pytest.raises(RuntimeError):
            Tweets(config_file)


class TestTweetGrab(TestTwitterAPIBase):
    def test_sds(self):
        num_sds_tweets = 100
        sds_tweets = self.t.grab_tweets("SDS", num_tweets=num_sds_tweets)
        assert len(sds_tweets) == num_sds_tweets

    def test_fake_twitter(self):
        """ Testing pulling tweets from an account that does not exist """
        fake_twitter_name = "ijljkl;j"
        with pytest.raises(tweepy.error.TweepError):
            self.t.grab_tweets(fake_twitter_name, num_tweets=10)

    def test_no_tweets(self):
        """ Testing pulling tweets from an account that has never tweeted """
        empty_twitter_name = "ShashankManjun5"
        tw = self.t.grab_tweets(empty_twitter_name, num_tweets=10)
        assert len(tw) == 0

    def test_num_tweets_100(self):
        """ Tests pulling default number of tweets """
        default_num_tweets = 100
        sds_tweets = self.t.grab_tweets("SDS")
        assert len(sds_tweets) == default_num_tweets

    def test_num_tweets_1(self):
        """ Test pulling a single tweet """
        num_tweets = 1
        sds_tweets = self.t.grab_tweets("SDS", num_tweets=num_tweets)
        assert len(sds_tweets) == num_tweets

    def test_num_tweets_0(self):
        """ Test pulling no tweets """
        num_tweets = 0
        sds_tweets = self.t.grab_tweets("SDS", num_tweets=num_tweets)
        assert len(sds_tweets) == num_tweets

    def test_num_tweets_36(self):
        """ Test pulling less than initial pull of tweets """
        num_tweets = 36
        sds_tweets = self.t.grab_tweets("SDS", num_tweets=num_tweets)
        assert len(sds_tweets) == num_tweets

    def test_num_tweets_112(self):
        """ Test pulling more than double initial pull of tweets """
        num_tweets = 112
        sds_tweets = self.t.grab_tweets("SDS", num_tweets=num_tweets)
        assert len(sds_tweets) == num_tweets

