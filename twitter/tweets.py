import configparser
import tweepy


class Tweets(object):
    """ Class to interact with Twitter API to pull tweets using Tweepy """
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = self.load_twitter_config()
        self.api = self.load_twitter_api()

    def load_twitter_api(self):
        """
        Helper function to load Tweepy API

        :return: Authenticated tweepy.api.API object
        """
        consumer_key = self.config["twitter"]["consumer_key"]
        consumer_key_secret = self.config["twitter"]["consumer_key_secret"]

        access_token = self.config["twitter"]["access_token"]
        access_token_secret = self.config["twitter"]["access_token_secret"]

        auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
        auth.set_access_token(access_token, access_token_secret)

        api = tweepy.API(auth)
        return api

    def grab_tweets(self, username, num_tweets=100):
        """
        Function to grab last num_tweets tweets for a given username

        :param username: Username of user for which tweets are to be pulled from
        :param num_tweets: Maximum number of tweets to grab. Defaults to 100.

        :return: List containing last num_tweets tweets from the given username
        """
        tweets = []

        # The tweepy User object allows us to access a given user's tweets
        user = self.api.get_user(username)

        tweets_to_pull = 50

        # If we want less than the minimum tweets to pull, we only pull that many tweets. If we want more than the
        # minimum tweets to pull, we repeatedly pull tweets until we have the desired number.

        # Ensuring that we are not pulling more than the total number of tweets that a user has tweeted
        if num_tweets == 0:
            return []

        if tweets_to_pull > user.statuses_count:
            tweets_to_pull = user.statuses_count
            num_tweets = user.statuses_count
        
        # Ensuring that we are not pulling more than the total number of desired tweets with our first twitter API call
        if tweets_to_pull > num_tweets:
            tweets_to_pull = num_tweets

        # Initial pull tweets
        pull_tweets = self.api.user_timeline(screen_name=username, count=tweets_to_pull)
        tweets += pull_tweets

        tweet_counter = 0

        # We ensure that we have both pulled more than zero tweets (if we pull zero, we have exhausted all the tweets to
        # pull), and that we have pulled less than the total number of tweets we want to pull
        while len(pull_tweets) > 0 and len(tweets) < num_tweets:
            pull_tweets = self.api.user_timeline(screen_name=username, count=tweets_to_pull)
            tweets += pull_tweets

            if len(tweets) >= num_tweets:
                # Cutting the total number of tweets down to the desired number of tweets
                tweets = tweets[:num_tweets]
                break

        return tweets

    def load_twitter_config(self):
        """
        Helper function to load Twitter config file

        :param config_file: String containing path to config file
        :return: ConfigParser object containing information from config file
        """
        config = configparser.ConfigParser(interpolation=None)
        config.read(self.config_file)
        
        # Since we are looking at the Twitter config file, it will by definition have the section "twitter". We want to
        # make sure that the user is not trying to use the default config file, so if the config parameter values start
        # with "< ", which is the default starting character for the unedited config file, we remind the user to set
        # their config file
        for k, v in config["twitter"].items():
            if v[:2] == "< ":
                raise RuntimeError("Config file parameter {} has default value - make sure you update the config file "
                "with the appropriate key values! See the README.md file for more details".format(k))
        return config

