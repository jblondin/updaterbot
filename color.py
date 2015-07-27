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
   Base RGB class 
   '''

   def __init__(self,red=0,green=0,blue=0,string=""):
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
      self.construct_from_rgb(*[int(color_str,16) for color_str in rgb_split])

   def validate_color(self,c,name):
      if c < 0 or c > 255:
         raise RGBError("Color parse error: {0} value out of range ({1}). Color values must be "
            "between 0 and 255 (inclusive)".format(name,c))

   def construct_from_rgb(self,red,green,blue):

      self.validate_color(red,"red")
      self.validate_color(green,"green")
      self.validate_color(blue,"blue")

      self._red = red
      self._green = green
      self._blue = blue

   @property
   def red(self):
      return self._red
   
   @property
   def green(self):
      return self._green
   
   @property
   def blue(self):
      return self._blue
