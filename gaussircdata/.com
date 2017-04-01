%chk=gaussianIRC.chk
%nproc=16
%mem=16GB
# BLYP/6-31g(d)//BLYP/TZP irc=(calcfc,maxpoint=400,forward) use=l115 nosymm SCF=Tight INT=UltraFine

IRC calculation for gaussian

0 0


C H O 0
6-31g(d)
****
Fe 0
TZP
****

Fe 0
TZP

