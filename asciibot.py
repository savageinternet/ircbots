import mechanize
import urllib

import tools.flickr as flickr

from basebot import BaseBot, startBot, parseArgs

ASCII_CONVERSION_URL = 'http://www.glassgiant.com/ascii/'

class AsciiBot(BaseBot):
  def get_picture_url_from_flickr_result(self, result):
      return result.getSmall()

  def get_ascii_for_URL(self, url):
    browser = mechanize.Browser()
    browser.open(ASCII_CONVERSION_URL)
    for form in browser.forms():
        ascii_art_form = form
    browser.form = ascii_art_form
    browser['webaddress'] = url
    response = browser.submit()
    image = response.read().split('<font face="monospace, Courier" size = "1" color = "000000">')[1]
    image = image.split('</font>')[0]
    image = image.replace('&nbsp;', ' ')
    image = image.replace('<br>', '\n')
    return image

  def _act(self, connection, target, message):
    search = message.lower().strip()
    print search
    photo = flickr.photos_search(text=search, license='cc', per_page=1)[0]
    photo_url = self.get_picture_url_from_flickr_result(photo)
    print photo_url
    art = self.get_ascii_for_URL(photo_url)
    print art
    connection.privmsg(target, art)

if __name__ == '__main__':
    options, args = parseArgs()
    startBot(AsciiBot, options)
