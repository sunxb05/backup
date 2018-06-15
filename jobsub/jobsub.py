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
for Index, Molecule in enumerate(ircRawList):
   fileDir  = os.path.join(currentPath, str(Index+1))
   os.mkdir(fileDir)
   os.chdir(fileDir)

   coordFile = open(str(Index+1) + '.xyz', "w")
   for atom in Molecule[1:]:
      for coordinate in atom:
         coordFile.write(coordinate + '   ')
      coordFile.write('\n')
   coordFile.close()

   infoFile  = open(str(Index+1)  + '.txt', "w")
   for term in Molecule[0]:
      infoFile.write(term + '   ')
   infoFile.close()

   if Molecule[0][0] == 'TS:':
      tsFile  = open(str(Index+1)  + '.ts', "w")
      tsLT = [Molecule[0][-12:][i:i+4] for i in [0,4,8]]
      for constaint in tsLT:
         for step in constaint:
            tsFile.write(step + '   ')
         tsFile.write('\n')
      tsFile.close()
      os.system('sh /home/x2sun/bin/jobsub/subts.sh *xyz *ts')
   else:
      os.system('sh /home/x2sun/bin/jobsub/subgo.sh *xyz')
   os.chdir(currentPath)
