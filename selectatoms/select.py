import sys, os
ircCoordFile  = sys.argv[1]
select =  sys.argv
# read xyz file like amv file exported from adfinput
ircFile = open(str(ircCoordFile))
ircRaw  = [[]]
for line in ircFile:
   llist = line.split()
   lllen = len(llist)
   if lllen == 4:
      # append coordinate
      ircRaw[-1].append(llist)
   else:
      # initiate new coordinate block
      ircRaw.append([])
ircRawList = [_f for _f in ircRaw if _f]
ircFile.close()

#select atoms
selectlist = []
for ircIndex, ircFrags in enumerate(ircRawList):
   xyzlist = []
   for i in select[2:]:
      xyzlist.append(ircFrags[int(i)-1])
   selectlist.append(xyzlist)

#Write into a text file
currentPath = os.getcwd()
fileName  = os.path.join(currentPath, str('selection.xyz'))
coordFile = open(str(fileName), "w")
for Index, Molecule in enumerate(selectlist):
   for atom in Molecule:
      for coor in atom:
         coordFile.write(str(coor) + '   ')
      coordFile.write('\n')
   coordFile.write('\n')
coordFile.close()
