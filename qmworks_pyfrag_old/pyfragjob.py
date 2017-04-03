from __future__ import unicode_literals

import os
import copy

from os.path import join as opj

from .basejob_1 import SingleJob
from .results import Results
from .settings import Settings
from .utils import PT
from .kftools import KFFile
from .errors import PlamsError

__all__ = ['pyfragjob']


#===================================================================================================
#===================================================================================================



class pyfragjob(SingleJob):
    """Abstract class gathering common mechanisms for jobs with all ADF Suite binaries."""
    _top = ['title','units','define']
    _command = ''
    _subblock_end = 'SubEnd'



    def get_input(self):
        """Transform all contents of ``setting.input`` branch into string with blocks, keys and values.

        On the highest level alphabetic order of iteration is modified: keys occuring in attribute ``_top`` are printed first.

        Automatic handling of ``molecule`` can be disabled with ``settings.ignore_molecule = True``.
        """

        def parse(key, value, indent=''):
            ret = ''
            key = key.title()
            if isinstance(value, Settings):
                ret += indent + key
                if '_h' in value:
                    ret += ' ' + value['_h']
                ret += '\n'

                i = 1
                while ('_'+str(i)) in value:
                    ret += parse('', value['_'+str(i)], indent+'  ')
                    i += 1

                for el in value:
                    if not el.startswith('_'):
                        ret += parse(el, value[el], indent+'  ')

                if indent == '':
                    ret += 'End\n'
                else:
                    ret += indent + self._subblock_end + '\n'
            elif isinstance(value, list):
                for el in value:
                    ret += parse(key, el, indent)
#            elif isinstance(value, (SCMJob, SCMResults, KFFile)):
#                ret += parse(key, value._settings_reduce(), indent)
            elif value is '' or value is True:
                ret += indent + key + '\n'
            else:
                value = str(value)
                ret += indent + key
                if key != '' and not value.startswith('='):
                    ret += ' '
                ret += value + '\n'
            return ret

        inp = ''
        inp += 'INPUT_SPECS\n\n'
#        use_molecule = ('ignore_molecule' not in self.settings) or (self.settings.ignore_molecule == False)
#        if use_molecule:
#            self._parsemol()
        for item in self._top:
            if item in self.settings.input:
                inp += parse(item, self.settings.input[item]) + '\n'
        for item in self.settings.input:
            if item not in self._top:
                inp += parse(item, self.settings.input[item]) + '\n'
        inp += 'END INPUT_SPECS\n\n'
        inp += '$ADFBIN/adf << eor\n'
        for item in self._top:
            if item in self.settings_2.input:
                inp += parse(item, self.settings_2.input[item]) + '\n'
        for item in self.settings_2.input:
            if item not in self._top:
                inp += parse(item, self.settings_2.input[item]) + '\n'

        inp += 'End Input\n'
        inp += 'eor'
#        if use_molecule:
#            self._removemol()


        return inp


    def get_runscript(self):
        """Generate a runscript. Returned string is of the form::

            $ADFBIN/name [-n nproc] <jobname.in [>jobname.out]

        ``name`` is taken from the class attribute ``_command``. ``-n`` flag is added if ``settings.runscript.nproc`` exists. ``[>jobname.out]`` is used based on ``settings.runscript.stdout_redirect``.
        """
        s = self.settings.runscript
        ret = '/scistor/tc/xsn800/bin/pyfrag.py'+self._command
        if 'nproc' in s:
            ret += ' -n ' + str(s.nproc)
#        ret += ' <'+self._filename('inp')
        ret += ' '+self._filename('inp')
        if s.stdout_redirect:
            ret += ' >'+self._filename('out')
        ret += '\n\n'
        return ret


    def check(self):
        """Check if ``termination status`` variable from ``General`` section of main KF file equals ``NORMAL TERMINATION``."""
#        try:
#            ret = (self.results.readkf('General', 'termination status').strip(' ') == 'NORMAL TERMINATION')
#        except:
#            return False
#        return ret
        pass

    def _parsemol(self):
        """Process |Molecule| instance stored in ``molecule`` attribute and add it as relevant entries of ``settings.input`` branch. Abstract method."""
#        raise PlamsError('Trying to run an abstract method SCMJob._parsemol()')
        pass 

    def _removemol(self):
        """Remove from ``settings.input`` all entries added by :meth:`_parsemol`. Abstract method."""
#        raise PlamsError('Trying to run an abstract method SCMJob._removemol()')
        pass

    def _settings_reduce(self):
        """When this object is present as a value in some |Settings| instance and string representation is needed, use the absolute path to the main KF file. See :meth:`Settings.__reduce__<scm.plams.settings.Settings.__reduce__>` for details."""
#        return self.results._kfpath()
        pass  

#===================================================================================================
#===================================================================================================


