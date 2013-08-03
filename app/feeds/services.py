from datetime import datetime
from dateutil import tz
import twitter

# I forgot how bad Python's date/time handling is.
def to_mst(date):
  from_tz = tz.tzutc()
  to_tz = tz.gettz('MST')

  date = date.replace(tzinfo=from_tz)
  mst = date.astimezone(to_tz)
  
  return mst

class Activity(object):
  def __init__(self, atype, title, message, date, url="#"):
    self.date = date 

    self.atype = atype
    self.title = title
    self.message = message
    self.url = url

  def __eq__(self, other):
    return self.date == other.date and self.title == other.title and self.message == other.message

class Feed(object):
  def __init__(self):
    self.activities = []

  def by_date(self): 
    return sorted(self.activities, key=lambda activity: activity.date)

class Tweets(Feed):
  def __init__(self, auth = {}):
    self.api = twitter.Api(
                           consumer_key = auth['consumer_key'],
                           consumer_secret = auth['consumer_secret'],
                           access_token_key = auth['access_token'],
                           access_token_secret = auth['access_secret']
                           )
    Feed.__init__(self)

  def pull(self, user):
    for a in self.api.GetUserTimeline(user):
      url = "https://twitter.com/%(user)s/status/%(status_id)i" % {"user": user, "status_id": a.id} 
      date = to_mst(self._parse_timestamp(a.created_at))
      title = "tweeted %s" % date.strftime("on %a %B %d, at %I:%M%p")

      activity = Activity('twitter', title, a.text, date, url)

      if activity not in self.activities:
        self.activities.append(activity)

    return self.activities

  def _parse_timestamp(self, time):
    return datetime.strptime(time, "%a %b %d %H:%M:%S +0000 %Y")

