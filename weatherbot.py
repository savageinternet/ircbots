from basebot import BaseBot, startBot, parseArgs
from xml.dom.minidom import parseString
import urllib
import urllib2
import re
import os.path

class WeatherBot(BaseBot):
  def _getData(self, root, key):
    return root.getElementsByTagName(key)[0].getAttribute('data')

  def _act(self, c, target, msg):
    params = urllib.urlencode({'q' : msg})
    url = 'http://www.google.com/ig/api?weather={0}'.format(params)
    f = urllib2.urlopen(url)
    try:
      xml = f.read()
      root = parseString(xml)
      forecast_information = root.getElementsByTagName(
          'forecast_information')[0]
      city = self._getData(forecast_information, 'city')
      current_conditions = root.getElementsByTagName('current_conditions')[0]
      temp_f = self._getData(current_conditions, 'temp_f')
      temp_c = self._getData(current_conditions, 'temp_c')
      humidity = self._getData(current_conditions, 'humidity')
      icon = self._getData(current_conditions, 'icon')
      rest, ext = os.path.splitext(icon)
      weather_type = os.path.basename(rest).replace('_', ' ')

      reply = 'the weather in {0} is currently {1}, {2} F ({3} C), {4}'.format(
          city, weather_type, temp_f, temp_c, humidity.lower())
      c.privmsg(target, reply)
    except KeyboardInterrupt:
      raise
    except:
      reply = "i'm having trouble with that one."
      c.privmsg(target, reply)
    finally:
      f.close()

if __name__ == '__main__':
  options, args = parseArgs()
  startBot(WeatherBot, options)
