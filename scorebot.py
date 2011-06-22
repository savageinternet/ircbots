from basebot import BaseBot, startBot, parseArgs

class ScoreBot(BaseBot):

  def _act(self, connection, target, message):
    person = message.split('++')
    connection.privmsg(target, answer)

if __name__ == '__main__':
    options, args = parseArgs()
    startBot(MyBot, options)
