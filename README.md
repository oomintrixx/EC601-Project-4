# EC601 Project 2

Shashank Manjunath  
manjuns@bu.edu  

## Introduction

This project tests out the Twitter API and the Google NLP API. In Part 1 of this project, we will create some simple
scripts to utilize some of the Twitter and Google NLP API functionality.


## Dependencies

This project uses:

```
python 3.6
tweepy
google-cloud-language
```

These packages can be installed using pip and the provided `requirements.txt` file using the command `pip install -r
requirements.txt`.

## API Key Setup

The Twitter API requires you to set up API keys. To do this, register your client application with twitter, and obtain
your Consumer Key and Consumer Secret Key, as well as your Access Token and Access Secret Token. More information on how
to obtain these keys can be found [here](https://developer.twitter.com/en/docs/twitter-api/getting-started/guide). Place
these into the config.ini file in the appropriate location.

The Google NLP API also requires setup. You will have to set up a Google Cloud project, and obtain the appropriate JSON
file with access tokens. More information can be found [here](https://cloud.google.com/natural-language/docs/setup).


## Testing out the APIs

As some background, I'm a massive college football fan, and I tend to root for Southeastern Conference (SEC) teams. I
also follow SaturdayDownSouth (@SDS on Twitter) for my SEC football news. For a quick demo to test out the Twitter API,
I will pull @SDS tweets, and if any of them refer to an SEC team, the program will analyze their sentiment towards or
against that team. The average sentiment across all tweets is then returned. The user story for this use case is as
follows:

I am a college football fan interested in learning what the media thinks of each SEC football team.

The `main.py` script exercises this functionality. It pulls the last N SaturdayDownSouth tweets (this is a user-defined
number), and analyzes the content of each tweet to generate a positive or negative sentiment for each team that is
tweeted about. It then prints each team's name, sentiment values, and an assessment of the overall sentiment for the
team to the console.

To run the `main.py` script, first set up your environment using `pip3` and the provided `requirements.txt` file. After
that, run the following command:

```
python main.py --num-tweets <number of tweets to pull> --twitter-api-config <path to twitter config> --cloud-api-config <path to cloud nlp json file>
```

Make sure to replace the `--twitter-api-config` and `--cloud-api-config` parameters with the correct filepaths as set up
in the API Key Setup section. The program should return something similar to the following:

```
Team:
Auburn
Score: 0.000    Magnitude: 0.050
This team has a Neutral sentiment.


Team:
Florida
Score: 0.000    Magnitude: 0.200
This team has a Mixed sentiment.


Team:
Georgia
Score: 0.150    Magnitude: 0.250
This team has a Clearly Positive sentiment.


Team:
Arkansas
Score: 0.200    Magnitude: 0.200
This team has a Clearly Positive sentiment.


Team:
University of Mississippi
Score: 0.050    Magnitude: 0.050
This team has a Neutral sentiment.


Team:
Kentucky
Score: 0.050    Magnitude: 0.050
This team has a Neutral sentiment.


Team:
Alabama
Score: -0.050   Magnitude: 0.050
This team has a Neutral sentiment.
```



