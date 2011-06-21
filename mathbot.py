import time
import urllib
import urllib2

from basebot import BaseBot, startBot, parseArgs

GOOGLE = 'http://www.google.com/ig/calculator?hl=en&q='

class MathBot(BaseBot):
  def _act(self, connection, target, message):
    search = message.lower().strip()
    print search
    math_url = GOOGLE + urllib.quote(search)
    f = urllib2.urlopen(math_url)
    json_response = f.read()
    f.close()
    answer = json_response.split('rhs: "')[1].split('",')[0]
    connection.privmsg(target, answer)

if __name__ == '__main__':
    options, args = parseArgs()
    startBot(MathBot, options)
