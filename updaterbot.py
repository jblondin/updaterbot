'''
Twitter bot that updates a profile image
'''

from PIL import Image
import array
import duration
from twitterbot import TwitterBot

class UpdaterBot(TwitterBot):

   def on_update(self):
      pixels = array.array('B',[255,0,0]*256**2)
      img = Image.frombytes('RGB',(256,256),pixels)
      image_filename="foo.png"
      img.save(image_filename)

if __name__ == "__main__":
   bot = UpdaterBot("updater.oauth",period_between_tweets=duration.Duration(minutes=1))
   bot.run()
