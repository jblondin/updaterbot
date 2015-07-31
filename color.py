'''
Utility classes for handling colors
'''

class RGBError(Exception):
  '''Base class for Color errors'''

  @property
  def message(self):
    '''Returns the first argument used to construct this error.'''
    return self.args[0]

class RGB(object):
   '''
   Base RGB class for 8-bit colors
   '''

   def __init__(self,red=-1,green=-1,blue=-1,string=""):
      '''
      RGB constructor
      '''
      if len(string) > 0:
         self.construct_from_string(string)
      else:
         self.construct_from_rgb(red,green,blue)

   def construct_from_string(self,string):
      # remove spaces
      string = "".join(string.split())
      
      if "," in string:
         self.construct_from_triplet(string)
      else:
         self.construct_from_hexcode(string)

   def construct_from_triplet(self,string):
      # remove parentheses
      string = "".join(string.split("("))
      string = "".join(string.split(")"))

      # split on commas
      colors = string.split(",")

      if len(colors) != 3:
         raise RGBError("Color parse error: invalid triplet format: {0}".format(string))

      self.construct_from_rgb(*[int(c) for c in colors])

   def construct_from_hexcode(self,string):
      # remove hash symbol
      string = "".join(string.split("#"))
      # remove '0x' at beginning
      string = "".join(string.split("0x"))

      if len(string) != 6:
         raise RGBError("Color parse error: invalid hexcode: {0}".format(string))

      rgb_split = [string[0:2],string[2:4],string[4:6]]
      try:
         self.construct_from_rgb(*[int(color_str,16) for color_str in rgb_split])
      except ValueError:
         raise RGBError("Color parse error: invalid hexcode: {0}".format(string))

   def is_valid(self):
      return self._red >= 0 and self._red < 256 and self._green >= 0 and self._green < 256 and \
         self._blue >= 0 and self._blue < 256

   def construct_from_rgb(self,red,green,blue):
      self._red = red
      self._green = green
      self._blue = blue

   @classmethod
   def clone(cls, instance):
      return cls(instance.red,instance.green,instance.blue)

   @property
   def red(self):
      return self._red
   @red.setter
   def red(self,r):
      self._red=r
   
   @property
   def green(self):
      return self._green
   @green.setter
   def green(self,g):
      self._green=g
   
   @property
   def blue(self):
      return self._blue
   @blue.setter
   def blue(self,b):
      self._blue=b

   def set(self,r,g,b):
      self._red=r
      self._green=g
      self._blue=b

   def list(self):
      return [self._red,self._green,self._blue]
   def tuple(self):
      return (self._red,self._green,self._blue)

   def __str__(self):
      return "({0},{1},{2})".format(self._red,self._green,self._blue)
