from basebot import BaseBot, startBot, parseArgs

class MyBot(BaseBot):

  def _act(self, connection, target, message):
    answer = 'hello world'
    connection.privmsg(target, answer)

if __name__ == '__main__':
    options, args = parseArgs()
    startBot(MyBot, options)
