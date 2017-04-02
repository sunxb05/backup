compared with qmworks source code,
add main PyFrag module PyFragModules.py into packages,
create new class Package_pyfrag in packages.py, and put it in registry()

def registry():
    """
    This function pass to the noodles infrascture all the information
    related to the Structure of the Package object that is schedule.
    This *Registry* class contains hints that help Noodles to encode
    and decode this Package object.
    """
    return Registry(
        parent=serial.base() + arrays_to_hdf5(),
        types={
            Package: AsDict(Package),
            Package_pyfrag: AsDict(Package_pyfrag),
            Path: SerPath(),
            plams.Molecule: SerMolecule(),
            Chem.Mol: SerMol(),
            Result: SerStorable(Result),
            Settings: SerSettings()})

create class PyFrag(Package_pyfrag) to call pyfrag module 

from qmworks.packages.packages import (Package,Package_pyfrag, package_properties, Result)
from qmworks.packages.PyFragModules import PyFragJob
import builtins
import plams
from plams import Molecule
# ========================= ADF ============================

class PyFrag(Package_pyfrag):
    """
    This class takes care of calling the *ADF* quantum package.
    it uses both Plams and the Templates module to create the input
    files, while Plams takes care of running the Job.
    It returns a ``ADF_Result`` object containing the output data.
    """
    def __init__(self):
        super(PyFrag, self).__init__("pyfrag")
        self.generic_dict_file = 'generic2pyfrag.json'

    def prerun(self):
        pass

    def run_job(self, settings,  settings_2=None, inputArgues=None, other = None, job_name='', **kwargs):
        """
        Execute ADF job.
        :param settings: user input settings.
        :type settings: |Settings|
        :param mol: Molecule to run the simulation
        :type mol: Plams Molecule
        :parameter input_file_name: The user can provide a name for the
                                    job input.
        :type input_file_name: String
        :parameter out_file_name: The user can provide a name for the
                                  job output.
        :type out_file_name: String
        :returns: :class:`~qmworks.packages.SCM.ADF_Result`
        """


        fragmentset = Settings()
        complexset  = Settings()
        fragmentset.input = settings.specific.fragment
        complexset.input  = settings_2.specific.complex
        job = PyFragJob(fragmentset, complexset, inputArgues, other)
        result = job.run()
        return result


add to data/templates complex.json and fragment.json and irc.json to handle the specific parameters

add to data/dictionaries generic2pyfrag.json to handle the term translation

finally to change json in templates/templates.py:

__all__ = ['freq', 'geometry', 'singlepoint', 'ts', 'get_template', 'fa', 'frag', 'irc']

# ================> Python Standard  and third-party <==========

from os.path import join
import json
import pkg_resources as pkg
#  ==================> Internal Modules  <=====================
from qmworks.utils import dict2Setting
# ==================================================


def get_template(template_name):
    """
    The function :func:`pkg_resources.resource_string` search for the location
    of the ``template_name`` file inside the installation directory an returns
    a strings with its contain. This string is subsequently converted in a
    python *dict* object using :func:`json.loads` and finally recursively
    transform into a |Settings| object.
    Using this function there are created the default templates for the
    following common calculations:
    * Singlepoint
    * Geometry optimization
    * Transition State optimization
    * Frequencies
    """
    path = join("data/templates", template_name)
    xs = pkg.resource_string("qmworks", path)
    s = json.loads(xs.decode())  # Json object must be string
    return dict2Setting(s)


# Generic Templates
singlepoint = get_template('singlepoint.json')
geometry = get_template('geometry.json')
ts = get_template('ts.json')
freq = get_template('freq.json')
irc  = get_template('irc.json')
fa   = get_template('complex.json')
frag = get_template('fragment.json')
