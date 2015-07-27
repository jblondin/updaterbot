import unittest
from color import RGB, RGBError

class TestRGB(unittest.TestCase):
   def test_rgb_from_colors(self):
      c = RGB()
      self.assertEquals(c.red,0)
      self.assertEquals(c.green,0)
      self.assertEquals(c.blue,0)

      c = RGB(red=11,green=22,blue=33)
      self.assertEquals(c.red,11)
      self.assertEquals(c.green,22)
      self.assertEquals(c.blue,33)

      c = RGB(green=22,red=11,blue=33)
      self.assertEquals(c.red,11)
      self.assertEquals(c.green,22)
      self.assertEquals(c.blue,33)

      with self.assertRaises(RGBError):
         RGB(red=256,green=44,blue=55)

   def test_rgb_from_triplet(self):
      c = RGB(string="11,22,33")
      self.assertEquals(c.red,11)
      self.assertEquals(c.green,22)
      self.assertEquals(c.blue,33)

      c = RGB(string="(11,22,33)")
      self.assertEquals(c.red,11)
      self.assertEquals(c.green,22)
      self.assertEquals(c.blue,33)

      with self.assertRaises(RGBError):
         RGB(string="11,22,33,44")

      with self.assertRaises(RGBError):
         RGB(string="11,22,333")

   def test_rgb_from_hexcode(self):
      c = RGB(string="#0B1621")
      self.assertEquals(c.red,11)
      self.assertEquals(c.green,22)
      self.assertEquals(c.blue,33)

      c = RGB(string="0x0B1621")
      self.assertEquals(c.red,11)
      self.assertEquals(c.green,22)
      self.assertEquals(c.blue,33)

      with self.assertRaises(RGBError):
         RGB(string="#0B162133")

      with self.assertRaises(RGBError):
         RGB(string="#0B160")

if __name__ == "__main__":
   # run unit tests
   unittest.main()
