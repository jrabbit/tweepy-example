import tweepy
import toml
import arrow
import logging
from typing import List, Union, Dict


logger = logging.getLogger(__name__)
OUR_CONF = "frogborg.toml"

def get_tweets(api) -> List[tweepy.Status]:
    try:
        public_tweets = api.home_timeline()
        return public_tweets
    except tweepy.error.RateLimitError:
        logger.info("Hit rate-limit.")
    except ConnectionError as e:
        logger.info("ConnectionError: %s", e)
    except tweepy.error.TweepError as e:
        logger.info("Other TweepyError: %s", e)
    return []

def handle_tweet(tweet) -> None:
    print(tweet)

def start(settings) -> None:
    auth = tweepy.OAuthHandler(settings['twitter']['auth']['consumer_key'], settings['twitter']['auth']['consumer_secret'])
    auth.set_access_token(settings['twitter']['auth']['access_token'], settings['twitter']['auth']['access_token_secret'])

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    me = api.me()
    logger.info("Got API, starting twitter module...")
    while True:
        for t in get_tweets(api):
            handle_tweet(t)
        last_look = arrow.utcnow()
        logger.debug("Sleeping for {} seconds".format(settings['twitter']['cooldown']))
        time.sleep(settings['twitter']['cooldown'])

if __name__ == "__main__":
    settings = toml.load(OUR_CONF)
    start(settings)