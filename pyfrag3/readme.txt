Pyfrag 3
Authors: Willem-Jan van Zeist, Lando P. Wolters
Current Development: Xiaobo Sun (x2.sun@vu.nl)

This program has the following functionalities:
1: Reads in a series of Linear Transit or IRC structures (coordinate files or t21).
2: For each point PyFrag generates single point calculations for the individual fragments (based on user defined fragments)
   and the whole complex system.
3: In the following the corresponding ADF calculations are conducted.
4: The program will generate a text file containing the decomposition energies plus other, user defined, values such as the strain energy.

Include python2 and python3 version, either can be used from command line or called from other program like qmworks.

Example use:
startpython PyFrag.py  --ircpath structuresIRC_CH3N.irc --fragment 1 3 4 --fragment 2 5 --strain 0 --strain 0 --adfinput basis.type=DZ

For the earlier version (PyFrag 2.0) please see http://www.few.vu.nl/~wolters/pyfrag/
