 PyFrag can also run in line with other types of computations like geometry optimization and IRC, in the same framework like PLAMS and QMWorks, both of which can tackle the construction and efficient execution of computational chemistry workflows. This provides a possibility to streamline all different computational jobs in one input and relief chemists of tedious jobs management procedures. With this purpose on mind, the PyFrag should be implemented as a module in PLAMS and QMWorks. This may seems a little tricky and complicated, especially for beginners. Also notice QMWorks itself is a developing program and some update later may be needed. The following input example shows how to call PyFrag in QMWorks.  To run PyFrag with other types of calculation and prepare more complex input, one should reference to the documents of PLAMS (https://www.scm.com/doc/plams/) and QMWorks (https://github.com/SCM-NV/qmworks).


Basically, this hack firstly change SMILE to json, and read son later to provide fragment information by pf module to plams.
now new basejob_1 run tis calculation by calling old pyfrag2.


In order to use PyFrag in QMWorks and PLAMS, the related modules should be placed in the right directory. The first part is the address of directory for QMWorks or PLAMS, what follows are the modules of PyFrag that can be found in the same directory where the current documentation is.

plams                                       basejob_1.py         pyfragjob.py
qmworks/data/templates          py.json                  irc.json     
qmworks/templates                 atoms.py                templates.py
qmworks/packages                  packages.py           SCM.py


The last step is to set up the address of your pyfrag source code. Open pyfragjob.py and change the right address according to your situation.

Similarly, set up the address in the “atoms.py” module that takes care of definition of fragments.

