import os
import sys
import types
from scm.plams import *

def collectarg( rawText, sep, dec='' ):
   a = rawText.split(sep, 1)
   if len( a ) < 2:
      return a[0]
   else:
      return a[0]+'='+dec+a[1].strip('\'')+dec

def parsearg( arg, optionlist, variatlist, outputlist, headerlist, programcmd ):
   if arg[0] == 'h':
      print '\n L.O.T.T.S. - Lord Of The Testing Scripts\n'
      print '-h                                                       this very help screen'
      print '-i.<InputOption>=<InputValue>                            translates to "set.input.<InputOption>=<InputValue>'
      print '-v.<VariableOption>=<InputValue1>,<InputValue2>,...      separate calculation with each "set.input.<VariableOption>=<InputValue1>'
      print '-o.<kfSection>.<kfVariable>                              translates to "result.readkf(<kfSection>, <kfVariable>)"'
      print '-g.<Quantity>                                            translates to "grep <Quantity> <OutputFile>"'
      print '-p.<Program>                                             ADF, BAND, or DFTB'
      print '-t.<TemplateFile>                                        reads file <TemplateFile> that may contain some of the above options (with or without initial "-")\n'
      sys.exit()

   elif arg[0] == 'i':
      optionlist.append('set.input.'+collectarg(arg[2:], '=', '"') )

   elif arg[0] == 'v':
      key, value = arg[2:].split( '=', 1 )
      variatlist = ['set.input.'+key+'="'+_.strip('\'')+'"' for _ in value.split(',')]
      headerlist[1] = key

   elif arg[0] == 'o':
      a, b = arg[2:].split('.')
      headerlist.append( a+'%'+b )
      outputlist.append( 'res.readkf("'+a+'", "'+b+'")' )

   elif arg[0] == 'g':
      a = arg[2:]
      headerlist.append( a )
      outputlist.append( 'res.grep_output(pattern="'+a+'")[-1].split("'+a+'", 1)[1].split()[0]' )

   elif arg[0] == 'p':
      programcmd = arg[2:]

   return optionlist, variatlist, outputlist, headerlist, programcmd

resultlist = []
systemlist = []
optionlist = []
variatlist = []
outputlist = []
headerlist = ['TESTSYSTEM', '']
programcmd = 'DFTB'
for arg in sys.argv[1:]:
   if   arg[:2] == '-t':
     if os.path.isfile( arg[3:] ):
        f = open( arg[3:] )
        for line in f.readlines():
           if line[0] == '-':
              line.lstrip('-')
           optionlist, variatlist, outputlist, headerlist, programcmd = parsearg( line.rstrip('\n'), optionlist, variatlist, outputlist, headerlist, programcmd )

   elif arg[0] == '-':
     optionlist, variatlist, outputlist, headerlist, programcmd = parsearg( arg[1:], optionlist, variatlist, outputlist, headerlist, programcmd )

   elif os.path.isfile( arg ) and os.path.splitext( arg )[1] == '.xyz':
      systemlist.append( os.path.abspath( arg ) )

   elif os.path.isdir( arg ):
      for file in os.listdir( arg ):
         if os.path.splitext( file )[1] == '.xyz':
            systemlist.append( os.path.join(arg, file) )

if (len(systemlist) > 0 and len(variatlist) > 0):
   init()
else:
   print systemlist
   print variatlist

widthlist = [len(_) for _ in headerlist]
for system in systemlist:
   for variation in variatlist:
      resultline   = [system.rsplit('/', 1)[1], variation.rsplit('=', 1)[1]]
      print resultline[0], resultline[1],

      try:
         mol = Molecule( system )

         set = Settings()

         for option in optionlist:
            exec option
         exec variation

         exec 'job = '+programcmd+'Job(molecule=mol, settings=set)'

         res = job.run()
         if job.check():
            for output in outputlist:
               try:
                  tmp = eval( output )
               except:
                  tmp = 'N.A.'
               resultline.append( str(tmp).rstrip() )
      except:
         print 'FAILING FOR', system, '|  variation', variation, '|  options',
         for option in optionlist:
            print option,
         print '| job = '+programcmd+'Job(molecule=mol, settings=set)'
         resultline.append( 'N.A.' )
      resultlist.append( resultline )
      for _ in range( len( resultline ) ):
         widthlist[_] = max(len(resultline[_]), widthlist[_])

line = '-'*(sum(widthlist)+4*len(widthlist))
print '\n', line
ii = 0
for entry in headerlist:
   print '  '+entry.ljust(widthlist[ii])+'  ',
   ii += 1
print '\n', line
for resultline in resultlist:
   ii = 0
   for result in resultline:
      print '  '+result.ljust(widthlist[ii])+'  ',
      ii += 1
   print ''
print line, '\n'

