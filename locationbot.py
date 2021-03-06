from basebot import BaseBot, startBot, parseArgs
import urllib

class LocationBot(BaseBot):
  def _act(self, connection, target, msg):
    params = urllib.urlencode({'q' : msg})
    url = 'http://maps.google.com?{0}'.format(params)
    connection.privmsg(target, url)

if __name__ == '__main__':
  options, args = parseArgs()
  startBot(LocationBot, options)
