import mechanize
import os.path
import sys

from ircbot import SingleServerIRCBot
from irclib import nm_to_n
from optparse import OptionParser

import tools.flickr as flickr

ASCII_CONVERSION_URL = 'http://www.glassgiant.com/ascii/'

class Asciibot(SingleServerIRCBot):
  def __init__(self, options):
    SingleServerIRCBot.__init__(
        self,
        [(options.host, options.port, None)],
        options.nick,
        options.nick)
    self._channels_to_join = [c.lower() for c in options.channels]

  def quit(self):
    self.connection.disconnect('bye')

  def get_ascii_for_URL(url):
    browser = mechanize.Browser()
    browser.open(ASCII_CONVERSION_URL)
    for form in b.forms():
        ascii_art_form = form
    browser.form = ascii_art_form
    browser['webaddress'] = url
    response = browser.submit()
    return response.read()

  def on_all_raw_messages(self, connection, event):
    message = event.arguments()[0]
    if 'asciibot:' in message.lower():
        search = message.lower().split('asciibot:')[1]
        photo = flickr.photos_search(text=search, per_page=1)[0]
        photo_url = photo.getURL()
        art = get_ascii_for_URL(photo_url)
        connection.privmsg(event.target, art)

  def on_welcome(self, connection, event):
    for channel in self._channels_to_join:
      connection.join(channel)

  def on_nicknameinuse(self, connection, event):
    connection.nick(connection.get_nickname() + '_')

  def on_invite(self, connection, event):
    connection.join(event.arguments()[0])

def main(options):
  bot = Logbot(options)
  try:
    bot.start()
  except KeyboardInterrupt:
    bot.quit()

def helpExit(msg):
  print msg
  sys.exit(1)

if __name__ == '__main__':
  parser = OptionParser()
  parser.add_option('--host', dest='host', help='host to connect to')
  parser.add_option('--port', dest='port', type='int',
      help='port to connect to')
  parser.add_option('--nick', dest='nick', default='asciibot',
      help='nick to join with')
  parser.add_option('--channel', dest='channels', action='append',
      help='channels to join')
  options, args = parser.parse_args()

  if not options.channels:
    helpExit('must specify at least one channel with --channel')

  main(options)
