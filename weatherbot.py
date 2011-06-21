from basebot import BaseBot, startBot, parseArgs
import urllib2

class WeatherBot(BaseBot):
  def _act(self, c, target, msg):
    c.privmsg('yeah, weatherbot is here')

if __name__ == '__main__':
  options, args = parseArgs()
  startBot(WeatherBot, options)
