import urllib2
import json
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
  """
    A wrapper for all activities or events from disparate services.
  """
  def __init__(self, atype, title, message, date, url="#"):
    self.date = date 

    self.atype = atype
    self.title = title
    self.message = message
    self.url = url

  def __eq__(self, other):
    return self.date == other.date and self.title == other.title and self.message == other.message

class Service(object):
  """
    Superclass for all services.  self.date_format arguably should be in Activity, but I'm keeping it here for now.
  """

  def __init__(self):
    self.activities = []
    self.date_format = "on %a %B %d, at %I:%M%p" 

  def _parse_service_timestamp(self, time):
    return datetime.strptime(time, self.service_time_format)

class GitHub(Service):
  """
    GitHub service.  acceptable is a map of event types (as defined by GitHub) to title formats.
    Probably should move the default definition elsewhere, but I like the dependency injection as it stands.
  """

  def __init__(self, acceptable = {'PushEvent': "Pushed a total of %(commit_count)i commit%(pluralize)s to %(repo)s %(date)s"}):
    self.acceptable = acceptable
    self.activity_url = "https://api.github.com/users/%s/events"
    self.service_time_format = "%Y-%m-%dT%H:%M:%SZ" 
    Service.__init__(self)

  def pull(self, user):
    request_url = self.activity_url % user
    events = json.loads(urllib2.urlopen(request_url).read())
    actionable = [event for event in events if event['type'] in self.acceptable.keys()]

    for activity in actionable:
      date = to_mst(self._parse_service_timestamp(activity['created_at']))
      message = ", ".join([commit["message"] for commit in activity["payload"]["commits"]])
      url = activity["repo"]["url"]

      title = self.acceptable[activity['type']] % {"commit_count": activity['payload']['size'], 
                                                   "pluralize": "s" if activity['payload']['size'] > 1 else "", 
                                                   "repo": activity["repo"]["name"],
                                                   "date": date.strftime(self.date_format)}

      activity = Activity('github', title, message, date, url)

      if activity not in self.activities:
        self.activities.append(activity)

    return self.activities

class Twitter(Service):
  """
    The service class for Twitter. Oh, OAuth, how I hate and love thee concurrently.
  """

  def __init__(self, auth = {}):
    self.api = twitter.Api(
                           consumer_key = auth['consumer_key'],
                           consumer_secret = auth['consumer_secret'],
                           access_token_key = auth['access_token'],
                           access_token_secret = auth['access_secret']
                           )
    self.service_time_format = "%a %b %d %H:%M:%S +0000 %Y" 

    Service.__init__(self)

  def pull(self, user):
    for a in self.api.GetUserTimeline(user):
      url = "https://twitter.com/%(user)s/status/%(status_id)i" % {"user": user, "status_id": a.id} 
      date = to_mst(self._parse_service_timestamp(a.created_at))
      title = "tweeted %s" % date.strftime(self.date_format)

      activity = Activity('twitter', title, a.text, date, url)

      if activity not in self.activities:
        self.activities.append(activity)

    return self.activities

