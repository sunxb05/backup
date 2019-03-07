#!/usr/bin/env python

import os, re, sys
#generate the dictionary between atomic number and atomic type
atomlist = {1:'H',3:'Li',4:'Be', 5:'B', 6:'C', 7:'N', 8:'O', 9:'F',11:'Na',12:'Mg',13:'Al',14:'Si', 15:'P',16:'S',17:'Cl', 26:'Fe',46:'Pd'}

input = open(sys.argv[1], 'r')
gsscript = input.read()
input.close()

#calculate the converged steps for every point of IRC
step  = re.compile(r'# OF STEPS ='+r'\s*\d*', re.DOTALL).findall(gsscript)
step  = ''.join(step)
step  = re.compile(r'# OF STEPS =', re.DOTALL).sub('',step)
step  = step.split()
step  = [int(x) for x in step]
number = 0
loop = []
for i in step:
   number+=i
   loop.append(number)
#collect coordinate of each points of IRC
data = []
for i in loop:
    spec = []
    if re.compile(r'Input orientation:', re.IGNORECASE).search(gsscript):
        if re.compile(r'Input orientation:', re.IGNORECASE).search(gsscript):
            testcace=re.compile(r'Input orientation:'+r'.*?'+ r'Distance matrix', re.IGNORECASE|re.DOTALL).findall(gsscript)
            spec = re.compile(r'Input orientation:'+r'.*?'+ r'Distance matrix', re.IGNORECASE|re.DOTALL).findall(gsscript)[i]
            spec = re.compile(r'Distance matrix (angstroms):'+r'.*', re.IGNORECASE).sub('', spec)
            spec = re.compile(r'Input orientation:'+r'.*', re.IGNORECASE).sub('', spec)
            newspec = []
            spec = spec.splitlines()[5:-2]
            atomnumber = len(spec)
            for line in spec:
                line = line.split()
                line = [atomlist[int(line[1])],line[3],line[4],line[5]]
                newspec.append(line)
            data.append(newspec)
#atomnumber = len(spec)
with open("irc_order.amv","a") as f:
     for i in range(len(loop)):
         # f.writelines("\n\n")
         f.writelines("\n")
         for j in range(atomnumber):
             f.writelines("\n")
             test= data[i][j]
             f.writelines(["%s " % item  for item in test])

f.close()
