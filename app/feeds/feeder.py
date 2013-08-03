import ConfigParser # I hate littering my environment with variables for configurable authentication, configs are easier for deployment and development purposes
from services import Tweets


def latest():
  config = ConfigParser.RawConfigParser()
  config.read('config/auth.cfg') # not ideal, but will fix soon

  tweets = Tweets({'consumer_secret': config.get('twitter', 'consumer_secret'),
                  'access_token': config.get('twitter', 'access_token'),
                  'consumer_key': config.get('twitter', 'consumer_key'),
                  'access_secret': config.get('twitter', 'access_secret')})

  return tweets.pull(config.get('twitter', 'shortname'))[:5]
