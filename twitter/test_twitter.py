from twitter.tweets import Tweets
import pytest


class TestTwitterAPIBase:
    VAR = 3
    DATA = 4

    def test_var_positive(self):
        assert self.VAR >= 0


class TestConfigLoading:
    """ Tests config file loading  """
    def test_empty_config(self):
        config_file = "tests/config_empty.ini"
        with pytest.raises(KeyError):
            Tweets(config_file)

    def test_empty_key_config(self):
        config_file = "tests/config_empty_2.ini"
        with pytest.raises(RuntimeError):
            self.assertTrue(Tweets(config_file))

    def test_default_config(self):
        config_file = "config.ini"
        with pytest.raises(RuntimeError):
            Tweets(config_file)


class TestTweetGrab(TestTwitterAPIBase):
    def test_sds(self):
        pass

    def test_fake_twitter(self):
        pass

    def test_num_tweets_100(self):
        """ Tests pulling default number of tweets """
        pass

    def test_num_tweets_1(self):
        """ Test pulling a single tweet """
        pass

    def test_num_tweets_0(self):
        """ Test pulling no tweets """
        pass

