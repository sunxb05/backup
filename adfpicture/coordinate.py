# read xyz file like amv file exported from adfinput
import os, string, re, sys
from shutil import copyfile
ircFile = open(sys.argv[1], 'r')
ircRaw  = [[]]
for line in ircFile:
   llist = line.split()
   lllen = len(llist)
   # if lllen == 4:
   if lllen != 0:
      # append coordinate
      ircRaw[-1].append(llist)
   else:
      # initiate new coordinate block
      ircRaw.append([])
ircRawList = [_f for _f in ircRaw if _f]
ircFile.close()

currentPath = os.getcwd()
fileDir  = os.path.join(currentPath, "Coordinatefile")
os.mkdir(fileDir)
os.chdir(fileDir)

for Index, Molecule in enumerate(ircRawList):
   coordFile = open(str(Index+1) + '.xyz', "w")
   for atom in Molecule[1:]:
      for coordinate in atom:
         coordFile.write(coordinate + '   ')
      coordFile.write('\n')
   coordFile.close()
