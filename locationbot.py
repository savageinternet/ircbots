from ircbot import SingleServerIRCBot
from irclib import nm_to_n
from optparse import OptionParser
import urllib
import sys

class Locationbot(SingleServerIRCBot):
  def __init__(self, options):
    SingleServerIRCBot.__init__(
        self,
        [(options.host, options.port, None)],
        options.nick,
        options.nick)
    self._channels_to_join = [c.lower() for c in options.channels]

  def quit(self):
    self.connection.disconnect('bye')

  def on_welcome(self, c, e):
    for channel in self._channels_to_join:
      c.join(channel)

  def on_nicknameinuse(self, c, e):
    c.nick(c.get_nickname() + '_')

  def on_invite(self, c, e):
    c.join(e.arguments()[0])

  def on_pubmsg(self, c, e):
    message = e.arguments()[0].strip()
    signal = options.nick + ':'
    if not message.startswith(signal):
      return
    location = message[len(signal):].strip()
    params = urllib.urlencode({'q' : location})
    url = 'http://maps.google.com?{0}'.format(params)
    c.privmsg(e.target(), url)

def main(options):
  bot = Locationbot(options)
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
  parser.add_option('--nick', dest='nick', default='locationbot',
      help='nick to join with')
  parser.add_option('--channel', dest='channels', action='append',
      help='channels to join')
  options, args = parser.parse_args()

  if not options.channels:
    helpExit('must specify at least one channel with --channel')

  main(options)
