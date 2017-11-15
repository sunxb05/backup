#!/usr/bin/env python3
# change bond length of two atom
# python3 bondlength.py  old.xyz   new.xyz   400    0.5    3.0

import sys, copy
coorfile  = sys.argv[1]
newfile   = sys.argv[2]
points    = int(sys.argv[3])
start     = float(sys.argv[4])
end       = float(sys.argv[5])

def Coordinate(coorFile, startPoint, endPoint, numPoint):
   ircRaw  = []
   ircList = []
   ircFile = open(coorFile, 'r')
   for line in ircFile:
      llist = line.split()
      llen = len(llist)
      if llen == 4:
         ircRaw[-1].append(llist)
      else:
         ircRaw.append([])
   ircRawList = [_f for _f in ircRaw if _f]
   ircRawList = [ircRawList * numPoint][0]
   step       = float(endPoint - startPoint) / numPoint
   for index, geometry in enumerate(ircRawList):
      geometry[1][1] = startPoint + step * (index + 1)
      ircList.append(copy.deepcopy(geometry))
   ircFile.close()
   return ircList

def WriteTable(tableValues, fileName):
   energyfile  = open(fileName, "w")
   for point in tableValues:
      for entry in point:
         writeKey(energyfile, entry)
      energyfile.write('\n')
   energyfile.close()

def writeKey(file, value, ljustwidth=16):
   for val in value:
      file.write(str.ljust(str(val), ljustwidth))
   file.write('\n')

WriteTable(Coordinate(coorfile, start, end, points), newfile)
