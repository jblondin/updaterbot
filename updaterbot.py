'''
Twitter bot that updates a profile image
'''

from PIL import Image
import array
import duration
from twitterbot import TwitterBot
from color import RGB

class UpdaterBot(TwitterBot):

   def on_subclass_init(self,**kwargs):
      self._step_size=10
      self._target_color=RGB(0,255,0)
      self._current_color=RGB(255,0,0)
      self._next_color=RGB(0,0,255)
      self._update_period=duration.Duration(minutes=30)
      self._nag_period=duration.Duration(hours=6)

   def on_update(self):
      pixels = array.array('B',[255,0,0]*256**2)
      img = Image.frombytes('RGB',(256,256),pixels)
      image_filename="foo.png"
      img.save(image_filename)
      self._running=False

if __name__ == "__main__":
   bot = UpdaterBot("updater.oauth",period_between_tweets=duration.Duration(minutes=1))
   bot.run()
