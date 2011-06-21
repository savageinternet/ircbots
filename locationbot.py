from basebot import BaseBot, startBot, parseArgs
import urllib

class LocationBot(BaseBot):
  def _act(self, c, target, msg):
    params = urllib.urlencode({'q' : msg})
    url = 'http://maps.google.com?{0}'.format(params)
    c.privmsg(target, url)

if __name__ == '__main__':
  options, args = parseArgs()
  startBot(LocationBot, options)
