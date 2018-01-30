##
# 
# Created by:  Bigendian Smalls
# Date:        Jan, 2018
# This is the 'brute forcer' for the ICHDEX01 RACF masking algorithm
# the algorithm can be quickly reversed by just checking plains in 
# individual positions with their encoded counterpart, as they do
# not change.
#     e.g.   A12345 = D5D0D382B524BC4C
#            AZZZZZ = D5CA4A4A4A4AFC4C
# 
#   Note the "D5" in the starting position for both.  Corresponding
#   plains with characters in the same position will yield a masked
#   hash the same output bytes.  Initially only upper and digits and
#   specials were available, but you can tweak easily to include 
#   lowers and others if you need to.
#
#   Input - expects the 8 byte mask hash as a 16 byte hex-encoded string
##



from ichdex01 import ichdex01
import sys

#from a2e_converter import *

def dec(masked):
  UL = 65
  UH = 90
  DL = 48
  DH = 57
  S1 = ord('@')
  S2 = ord('#')
  S3 = ord('$')

  c = list()

# add uppers
  for i in range(UL,UH+1):
      c.append(chr(i))

# add digits
  for i in range(DL,DH+1):
      c.append(chr(i))

# add specials
  c.append(chr(S1))
  c.append(chr(S2))
  c.append(chr(S3))

  re = ichdex01()

  # PASSWORD
  plain = ""

  ehash = masked.decode('hex')
  for j in range(0,8):
    echar = ehash[j]
    if echar == '\x4c':
      break
    #print("checking pos {0:02X}".format(ord(echar)))
    for i in range(0,len(c)):
      tchar = c[i]
      x = re.enc(plain + tchar)
      #print(x[0:(j*2)+2] + ":" + echar.encode('hex'))
      if x[j*2:(j*2)+2].decode('hex')==echar:
        #print("Found position #{0:d} is {1:s}".format(j, c[i]))
        plain = plain + c[i]
        break

  return plain

if __name__ == "__main__":
  if(len(sys.argv) > 1):
    val = sys.argv[1].upper()
    if len(val) != 16:
      print("Hash is too short, must be = 16")
      sys.exit()
    print dec(val)
  else:
    tests = ["F09B70807C4C4C4C","C16337002C4C4C4C","F5478251A02C4C4C"]
    for i in tests:
      print("Test hash {0:s} is plain \'{1:s}\'".format(i, dec(i)))
