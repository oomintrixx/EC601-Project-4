from cloud_nlp.sentiment_analysis import SentimentAnalyzer, SentimentContainer
from twitter.tweets import Tweets

from collections import defaultdict
from itertools import chain
from tqdm import tqdm
import argparse


# Dict to hold nicknames for SEC football teams
sec_football_names = {
    # Alabama
    "alabama": "Alabama", 
    # Arkansas
    "arkansas": "Arkansas",
    "razorbacks": "Arkansas",
    # Auburn
    "auburn": "Auburn",
    "tigers": "Auburn",
    # Florida
    "florida": "Florida",
    "gators": "Florida",
    # Georgia
    "georgia": "Georgia",
    "dawgs": "Georgia",
    "bulldogs": "Georgia",
    # Kentucky
    "kentucky": "Kentucky",
    # LSU
    "lsu": "LSU",
    # Mississippi
    "ole miss": "University of Mississippi",
    # Mississippi State
    "msu": "Mississippi",
    # Missouri
    "mizzou": "University of Missouri",
    # USC
    "sc": "South Carolina",
    "usc": "South Carolina",
    "gamecocks": "South Carolina",
    # Tennessee
    "tennessee": "Tennessee",
    # Texas A&M
    "texas a&m": "Texas A&M",
    "tamu": "Texas A&M",
    "aggies": "Texas A&M",
    # Vanderbilt
    "vanderbilt": "Vanderbilt",
    "vandy": "Vanderbilt",
}


def main(twitter_config_file, cloud_nlp_config_file, num_tweets):
    """
    Main function to run tweet analysis functionality

    :param twitter_config_file: String path to Twitter config file
    :param cloud_nlp_config_file: String path to Google Cloud NLP config file
    :param num_tweets: Number of tweets to analyze
    """
    # Setting up APIs with correct authentication
    tweets = Tweets(twitter_config_file)
    sentiment_analyzer = SentimentAnalyzer(cloud_nlp_config_file)

    # Grabbing the latest 100 tweets from @SDS
    user_tweets = tweets.grab_tweets(username="SDS", num_tweets=num_tweets)

    # Filtering strings for keywords we are interested in -- e.g. Vanderbilt University is sometimes referred to as
    # "Vandy", so we search for this string as well
    keywords = [x.lower() for x in sec_football_names.keys()]

    # Getting text of each tweet
    user_tweets_text = [x.text for x in user_tweets]

    # Creating container to hold tweets for each team
    team_sentiment = defaultdict(SentimentContainer)

    # Analyzing the sentiment of each relevant tweet
    for t in tqdm(user_tweets_text):
        # Analyzing entities in tweet
        tweet_entities = sentiment_analyzer.analyze_entities(t)

        for e in tweet_entities.entities:
            # Checking if entity is relevant based on keywords
            if e.name.lower() in keywords:
                team_name = sec_football_names[e.name.lower()]
                team_sentiment[team_name].add(e.sentiment)

    # Getting semantic meaning and printing sentiment analysis results
    for k, v in team_sentiment.items():
        semantic_sentiment = sentiment_analyzer.get_semantic_sentiment(v.calculate())
        print("Team:\n{}\nScore: {:.3f}\tMagnitude: {:.3f}\nThis team has a {} sentiment.\n\n".format(k,
            v.get_score(), v.get_magnitude(), semantic_sentiment))
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Program to analyze SaturdayDownSouth (@SDS) tweets about SEC "
            "Football")
    parser.add_argument("--twitter-api-config", metavar="T", type=str, required=True, help="Path to Twitter API config "
            "file")
    parser.add_argument("--cloud-api-config", metavar="C", type=str, required=True, help="Path to Cloud NLP json file")
    parser.add_argument("--num-tweets", metavar="N", type=int, required=True, help="Number of tweets to pull")
    args = parser.parse_args()
    main(args.twitter_api_config, args.cloud_api_config, args.num_tweets)

