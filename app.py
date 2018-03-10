import tweepy
import toml

OUR_CONF = "frogborg.toml"

def start(settings) -> None:
    auth = tweepy.OAuthHandler(settings['twitter']['auth']['consumer_key'], settings['twitter']['auth']['consumer_secret'])
    auth.set_access_token(settings['twitter']['auth']['access_token'], settings['twitter']['auth']['access_token_secret'])

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    me = api.me()
    logger.info("Got API, starting twitter module...")
    while True:
        for t in get_tweets():
            handle_tweet(t)
        last_look = arrow.utcnow()
        logger.debug("Sleeping for {} seconds".format(settings['twitter']['cooldown']))
        time.sleep(settings['twitter']['cooldown'])

if __name__ == "__main__":
    settings = toml.load(OUR_CONF)
    start(settings)