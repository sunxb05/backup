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


xyzlist = []
atomnumber = len(select[2:])
for ircIndex, ircFrags in enumerate(ircRawList):
      x = 0.0; y = 0.0; z = 0.0
      for i in select[2:]:
         x = x + float(ircFrags[int(i)-1][1])
         y = y + float(ircFrags[int(i)-1][2])
         z = z + float(ircFrags[int(i)-1][3])
      xyz = ["Xx",x/atomnumber,y/atomnumber,z/atomnumber]
      ircFrags.append(xyz)



currentPath = os.getcwd()
fileName  = os.path.join(currentPath, str('center.xyz'))
coordFile = open(str(fileName), "w")
for Index, Molecule in enumerate(ircRawList):
   for atom in Molecule:
      for coor in atom:
         coordFile.write(str(coor) + '   ')
      coordFile.write('\n')
   coordFile.write('\n')
coordFile.close()
