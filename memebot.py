from ircbot import SingleServerIRCBot
from irclib import nm_to_n
from optparse import OptionParser
import re
import sys

class BaseBot(SingleServerIRCBot):
  def __init__(self, options):
    SingleServerIRCBot.__init__(
        self,
        [(options.host, options.port, None)],
        options.nick,
        options.nick)
    self._nick = options.nick
    self._channels_to_join = [c.lower() for c in options.channels]
    if options.signal:
        self._signal = options.signal
    else:
        self._signal = self._nick + ':'

  def quit(self):
    self.connection.disconnect('bye')

  def on_welcome(self, c, e):
    for channel in self._channels_to_join:
      c.join(channel)

  def on_nicknameinuse(self, c, e):
    c.nick(c.get_nickname() + '_')

  def on_invite(self, c, e):
    c.join(e.arguments()[0])

  def _act(self, c, target, msg):
    pass

  def on_pubmsg(self, c, e):
    message = e.arguments()[0].strip()
    if not re.match(self._signal, message):
      return
    if self._signal == self._nick + ':':
        message_without_signal = message[len(self._signal):].strip()
        self._act(c, e.target(), message_without_signal)
    else:
        self._act(c, e.target(), message)

def startBot(bot_class, options):
  bot = bot_class(options)
  try:
    bot.start()
  except KeyboardInterrupt:
    bot.quit()

def parseArgs(parser=OptionParser()):
  def helpExit(msg):
    print msg
    sys.exit(1)

  parser.add_option('--host', dest='host', help='host to connect to')
  parser.add_option('--port', dest='port', type='int',
      help='port to connect to')
  parser.add_option('--nick', dest='nick', help='nick to join with')
  parser.add_option('--signal', dest='signal', help='regexp to match messages to listen to, default ^nick:')
  parser.add_option('--channel', dest='channels', action='append',
      help='channels to join')
  options, args = parser.parse_args()
  if not options.channels:
    helpExit('must specify at least one channel with --channel')
  return options, args
