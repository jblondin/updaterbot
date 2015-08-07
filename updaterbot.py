'''
Twitter bot that updates a profile image
'''

from PIL import Image
import array
import math
import twitter

from twitterbot import TwitterBot
import duration
import storage
import command
import timeutils

from color import RGB,RGBError

# profile image updated isn't in the version of python-twitter that pip installed...this is a 
# workaround
import base64
def UpdateProfileImage(api,image_filename):

  url = '%s/account/update_profile_image.json' % (api.base_url)
  with open(image_filename, 'rb') as image_file:
    encoded_image = base64.b64encode(image_file.read())
  data = {
    'image':encoded_image
  }
  json=api._RequestUrl(url, 'POST', data=data)
  if json.status_code in [200, 201, 202]:
    return True
  if json.status_code == 400:
    raise twitter.TwitterError({'message': "Image data could not be processed"})
  if json.status_code == 422:
    raise twitter.TwitterError({'message': "The image could not be resized or is too large."})

class StoredRGB(RGB,storage.StorageMixin):
   pass

class UpdaterBot(TwitterBot):

   def __init__(self,*args,**kwargs):
      super(UpdaterBot,self).__init__(*args,**kwargs)

      self._step_size=10
      if 'step_size' in kwargs:
         self._step_size=kwargs['step_size']
      self._update_period=duration.Duration(hours=2)
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

      # create separate twitter api object for profile we're updating
      if 'profile_oauth_file' not in kwargs:
         raise twitterbot.TwitterBotError("Unable to create UpdaterBot: no profile oauth provided")
      profile_oauth = storage.load_data(kwargs['profile_oauth_file'])
      self._profile_api = twitter.Api(**profile_oauth)
      self._profile_user = self._profile_api.VerifyCredentials()

      self._target_color_filename="target_color.dat"
      self._current_color_filename="current_color.dat"
      self._next_color_filename="next_color.dat"
      self._last_update_file="last_profile_update.dat"

      self._DEBUG=True

   def on_update_start(self):
      # read colors from file
      self._current_color=StoredRGB.load(self._current_color_filename)
      if not self._current_color.is_valid():
         # default to red
         self._current_color.set(255,0,0)
      self._target_color=StoredRGB.load(self._target_color_filename)
      if not self._target_color.is_valid():
         # default to purple
         self._target_color.set(255,0,255)
      self._next_color=StoredRGB.load(self._next_color_filename)
      if not self._next_color.is_valid():
         # default to unset
         self._next_color=None

   def on_update_end(self):
      if timeutils.time_since_file(self._last_update_file) > self._update_period.timedelta:
         before_str=str(self._current_color)
         self.update_current_color()
         print "Updated from {0} to {1}".format(before_str,str(self._current_color))
         self.post_profile_image(self.generate_image())
         timeutils.save_now_to_file(self._last_update_file)

      self._target_color.save(self._target_color_filename)
      self._current_color.save(self._current_color_filename)
      if self._next_color is not None:
         self._next_color.save(self._next_color_filename)

   def update_current_color(self):
      '''
      Calculates the new color to use.
      '''
      self._current_color = self._current_color # shortened name
      self._target_color = self._target_color # shortened name
      red_dist_sqrd=(self._current_color.red-self._target_color.red)**2
      green_dist_sqrd=(self._current_color.green-self._target_color.green)**2
      blue_dist_sqrd=(self._current_color.blue-self._target_color.blue)**2
      dist_sqrd=red_dist_sqrd+blue_dist_sqrd+green_dist_sqrd
      step_size=float(self._step_size)

      if dist_sqrd < step_size**2:
         # distance is less than step size, just move the rest of the way to the target by setting
         # current color to a copy of the target color
         self._current_color=StoredRGB.clone(self._target_color)
         if self._next_color is not None:
            self._target_color=StoredRGB.clone(self._next_color)
            self._next_color = None
      else :
         # distance is more than step size

         if dist_sqrd < (step_size*2)**2:
            # distance is less than twice step size.  Move half the distance to the target
            step_size = math.sqrt(dist_sqrd)/2

         # update current_color
         self._current_color.red=self.step_one_color(self._current_color.red,\
            self._target_color.red,step_size*red_dist_sqrd/dist_sqrd)
         self._current_color.green=self.step_one_color(self._current_color.green,\
            self._target_color.green,step_size*green_dist_sqrd/dist_sqrd)
         self._current_color.blue=self.step_one_color(self._current_color.blue,\
            self._target_color.blue,step_size*blue_dist_sqrd/dist_sqrd)

   def step_one_color(self,current,target,step_size):
      # quick and dirty sign function
      sign = lambda x: math.copysign(1, x)
      # quick and dirty squash funciton
      squash_to_8bit = lambda x: 0 if x < 0 else 255 if x > 255 else x

      val=int(squash_to_8bit(current+step_size*sign(target-current)))

      return val

   def generate_image(self):
      rgb = self._current_color.list()
      pixels = array.array('B',rgb*self._h*self._w)
      img = Image.frombytes('RGB',(self._h,self._w),pixels)
      image_filename="profile_image.png"
      img.save(image_filename)
      return image_filename

   def post_profile_image(self,image_filename):
      UpdateProfileImage(self._profile_api,image_filename)

   def set_next_color(self,color):
      self._next_color=color
      self._next_color.save(self._next_color_filename)
   def set_target_color(self,color):
      self._target_color=color
      self._target_color.save(self._target_color_filename)

class SetColorCommand(command.Command):
   def __init__(self,params,context):
      self._params=params
      self._bot=context

   def run(self):
      if len(self._params) == 0:
         return "Error: No color specified"
      try:
         clr=StoredRGB(string=self._params[0])
         self.set_color(clr)
         return "Color set to {0}".format(str(clr))
      except RGBError,err:
         return "Error: {0}".format(err.message)

   def set_color(self,clr):
      # implemented in subclass
      pass

class SetNextColorCommand(SetColorCommand):
   def set_color(self,clr):
      self._bot.set_next_color(clr)

class SetTargetColorCommand(SetColorCommand):
   def set_color(self,clr):
      self._bot.set_target_color(clr)

command.CommandFactory.commands['pi_set_target_color']=SetTargetColorCommand
command.CommandFactory.commands['pi_set_next_color']=SetNextColorCommand

if __name__ == "__main__":
   bot = UpdaterBot("updater.oauth",profile_oauth_file="jblondin.oauth",)
   bot.run()
