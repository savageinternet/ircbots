import datetime
import dateutil.parser
import urllib
import urllib2

from basebot import BaseBot, startBot, parseArgs

FUNCHEAP = 'http://sf.funcheap.com'
EVENT_FILE = 'events.csv'

NAME = 0
DATE = 1
LOCATION = 2

class EventBot(BaseBot):

  def _get_events(self):
    events = []
    f = open(EVENT_FILE, 'r+')
    for event_line in f:
        event_name, event_date, event_location = event_line.split(',')
        events.append((event_name, dateutil.parser.parse(event_date), event_location))
    f.close()
    return events

  def _remove_past_events(self, events):
    now = datetime.datetime.today()
    past = 0
    for idx in range(len(events)):
        if now > events[idx][DATE]:
            past += 1
    events = events[past:]
    return events

  def get_next_event(self, search):
    next_event = self._remove_past_events(self._get_events())[0]
    return 'next event is %s on %s at %s' % next_event

  def add_event(self, event):
    a_event_name, a_event_date, a_event_location = event.split(',')
    a_event_name = a_event_name.strip()
    a_event_date = a_event_date.strip()
    a_event_location = a_event_location.strip()
    a_event_date = a_event_date.replace('today', datetime.datetime.today().strftime('%Y-%m-%d'))
    a_event_date = a_event_date.replace('tomorrow', (datetime.datetime.today() +\
                                                     datetime.timedelta(1)).strftime('%Y-%m-%d'))
    try:
        a_event_date = dateutil.parser.parse(a_event_date)
    except ValueError:
        return 'date %s could not be parsed.  type eventbot: help if you need help.' % a_event_date
    events = self._remove_past_events(self._get_events())
    if len(events) > 0:
        for idx in range(len(events)):
            if events[idx][1] > a_event_date:
                events.insert(idx, (a_event_name, a_event_date, a_event_location))
                break
    else:
        events = [(a_event_name, a_event_date, a_event_location)]
    f = open(EVENT_FILE, 'w')
    for event in events:
        f.write('%s,%s,%s\n' %\
                    (event[NAME], event[DATE].strftime('%Y-%m-%d %H:%M'), event[LOCATION]))
    f.close()
    return 'event added'

  def _act(self, connection, target, message):
    message = message.lower().strip()
    action = message.split()[0]
    if action == 'help':
        answer = 'try eventbot:add event name, event date, event location OR eventbot: next'
    if action == 'add':
        answer = self.add_event(message[3:])
    if action == 'next':
        answer = self.get_next_event(message[4:])
    connection.privmsg(target, answer)

if __name__ == '__main__':
    options, args = parseArgs()
    startBot(EventBot, options)
