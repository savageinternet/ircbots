from ircbot import SingleServerIRCBot
from irclib import nm_to_n
from optparse import OptionParser
import os.path
import sys

class Logbot(SingleServerIRCBot):
  def __init__(self, options):
    SingleServerIRCBot.__init__(
        self,
        [(options.host, options.port, None)],
        options.nick,
        options.nick)
    self._log_file_name = options.file
    self._log_file = None
    self._channels_to_join = [c.lower() for c in options.channels]

  def quit(self):
    self.connection.disconnect('bye')
    if self._log_file is not None:
      self._log_file.close()

  def on_all_raw_messages(self, c, e):
    message = e.arguments()[0]
    print message
    if self._log_file is not None:
      self._log_file.write(message + '\n')

  def on_welcome(self, c, e):
    print e.arguments()
    if self._log_file_name is not None:
      self._log_file = open(self._log_file_name, 'w')
    for channel in self._channels_to_join:
      c.join(channel)

  def on_nicknameinuse(self, c, e):
    c.nick(c.get_nickname() + '_')

  def on_invite(self, c, e):
    c.join(e.arguments()[0])

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
  parser.add_option('--nick', dest='nick', default='logbot',
      help='nick to join with')
  parser.add_option('--channel', dest='channels', action='append',
      help='channels to join')
  parser.add_option('--file', dest='file', help='file to log to')
  options, args = parser.parse_args()

  if not options.channels:
    helpExit('must specify at least one channel with --channel')

  main(options)
