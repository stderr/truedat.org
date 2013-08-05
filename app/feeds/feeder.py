import ConfigParser # I hate littering my environment with variables for configurable authentication, configs are easier for deployment and development purposes
from services import Twitter, GitHub


def latest(limit=7):
  """
    Controller interface to feed services. Definitely needs a makeover.
  """

  config = ConfigParser.RawConfigParser()
  config.read('config/auth.cfg') # not ideal, but will fix soon

  tweeter = Twitter({'consumer_secret': config.get('twitter', 'consumer_secret'),
                  'access_token': config.get('twitter', 'access_token'),
                  'consumer_key': config.get('twitter', 'consumer_key'),
                  'access_secret': config.get('twitter', 'access_secret')})

  tweets = tweeter.pull(config.get('twitter', 'shortname'))[0:limit]

  github = GitHub()
  github_events = github.pull('stderr')

  merged = tweets + github_events
  return sorted(merged, key=lambda activity: activity.date, reverse=True)[0:limit]
