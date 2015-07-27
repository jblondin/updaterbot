'''
Twitter bot that updates a profile image
'''

from PIL import Image
import array
import duration
from twitterbot import TwitterBot
from color import RGB
import math

class StoredRGB(RGB,StorageMixin):
   pass

class UpdaterBot(TwitterBot):

   def on_subclass_init(self,**kwargs):
      self._step_size=10
      if 'step_size' in kwargs:
         self._step_size=kwargs['step_size']
      self._update_period=duration.Duration(minutes=30)
      if 'update_period' in kwargs:
         self._update_period=kwargs['update_period']
      self._nag_period=duration.Duration(hours=6)
      if 'nag_period' in kwargs:
         self._nag_period=kwargs['nag_period']
      self._h=256
      if 'h' in kwargs:
         self._h=kwargs['h']
      if 'height' in kwargs:
         self._h=kwargs['height']
      self._w=256
      if 'w' in kwargs:
         self._w=kwargs['w']
      if 'width' in kwargs:
         self._w=kwargs['width']

      self._target_color=StoredRGB(0,255,0)
      self._current_color=StoredRGB(255,0,0)
      self._next_color=None

   def on_update_start(self):
      pass

   def on_update_end(self):
      generate_image(self.step())

   def step(self):
      c1 = self._current_color
      c2 = self._target_color
      red_dist_sqrd=(c1.red-c2.red)**2
      green_dist_sqrd=(c1.green-c2.green)**2
      blue_dist_sqrd=(c3.blue-c3.blue)**2
      dist_sqrd=red_dist_sqrd+blue_dist_sqrd+green_dist_sqrd
      step_size=float(self._step_size)
      if dist_sqrd < step_size**2:
         # distance is less than step size, just move the rest of the way to the target by setting
         # current color to a copy of the target color
         self._current_color=StoredRGB.clone(c2)
         if self._next_color is not None:
            self._target_color=StoredRGB.clone(self._next_color)
            self._next_color = None
      else :
         # distnace is more than step size

         if dist_sqrd < (step_size*2)**2:
            # distance is less than twice step size.  Move half the distance to the target
            step_size = math.sqrt(dist_sqrd)/2

         # quick and dirty sign() function
         sign = lambda x: math.copysign(1, x)

         # update current_color
         red_step=step_size*red_dist_sqrd/dist_sqrd
         c1.red=c1.red+red_step*sign(c2.red-c1.red)
         green_step=step_size*green_dist_sqrd/dist_sqrd
         c1.green=c1.green+green_step*sign(c2.green-c1.green)
         blue_step=step_size*blue_dist_sqrd/dist_sqrd
         c1.blue=c1.blue+blue_step*sign(c2.blue-c1.blue)

      return self._current_color

   def generate_image(self,rgb):
      pixels = array.array('B',rgb.list()*self._h*self._w)
      img = Image.frombytes('RGB',(self._h,self._w),pixels)
      image_filename="profile_image.png"
      img.save(image_filename)
      return image

if __name__ == "__main__":
   bot = UpdaterBot("updater.oauth",update_period=duration.Duration(minutes=1))
   bot.run()
