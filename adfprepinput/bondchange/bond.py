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



coordFile = open("bond" + '.xyz', "w")
for Index, Molecule in enumerate(ircRawList):
  for atom in Molecule:
     for coordinate in atom[1:]:
        coordFile.write(coordinate + '   ')
     coordFile.write('\n')
  coordFile.write('\n\n\n')
coordFile.close()
