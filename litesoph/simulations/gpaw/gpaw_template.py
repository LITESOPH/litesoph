import pathlib
from typing import Any, Dict


class GpawGroundState:
    """This class contains the default parameters and the template for creating gpaw 
    scripts for ground state calculations."""
    default_param =  {
        'mode': 'fd',
        'xc': 'LDA',
        'occupations': None,
        'poissonsolver': None,
        'h': None,  # Angstrom
        'gpts': None,
        'kpts': [(0.0, 0.0, 0.0)],
        'nbands': None,
        'charge': 0,
        'setups': {},
        'basis': {},
        'spinpol': None,
        'filter': None,
        'mixer': None,
        'eigensolver': None,
        'background_charge': None,
        'experimental': {'reuse_wfs_method': 'paw',
                         'niter_fixdensity': 0,
                         'magmoms': None,
                         'soc': None,
                         'kpt_refine': None},
        'external': None,
        'random': False,
        'hund': False,
        'maxiter': 333,
        'idiotproof': True,
        'symmetry': {'point_group': True,
                     'time_reversal': True,
                     'symmorphic': True,
                     'tolerance': 1e-7,
                     'do_not_symmetrize_the_density': None},  # deprecated
        'convergence': {'energy': 0.0005,  # eV / electron
                        'density': 1.0e-4,
                        'eigenstates': 4.0e-8,  # eV^2
                        'bands': 'occupied'},  # eV / Ang
        'verbose': 0,
        'fixdensity': False,  # deprecated
        'dtype': None}  # deprecated

    gs_template = """
from ase.io import read, write
from gpaw import GPAW
from numpy import inf

# Molecule or nanostructure
atoms = read('{geometry}')
atoms.center(vacuum={vacuum})

#Ground-state calculation
calc = GPAW(mode='{mode}',
    xc='{xc}',
    h={h},  # Angstrom
    gpts={gpts},
    kpts={kpts},
    nbands= {nbands},
    charge= {charge},
    setups= {setups},
    basis={basis},
    spinpol= {spinpol},
    filter={filter},
    mixer={mixer},
    hund={hund},
    maxiter={maxiter},
    symmetry={symmetry},  
    convergence={convergence},
    txt='gs.out')
atoms.calc = calc
energy = atoms.get_potential_energy()
calc.write('gs.gpw', mode='all')

    """
    def __init__(self, user_input) -> None:
        self.user_input = self.default_param
        self.user_input.update(user_input)

    # def check(self)-> bool:
    #     """checks whether user given input parameters is compatable with with gpaw ground state calculation"""

    #     if self.user_input['mode'] not in ['fd', 'lcao', 'pw'] and  self.user_input['engine'] == 'gpaw':
    #         raise ValueError('This mode is not compatable with gpaw use fd, lcao or paw')
        
    #     if self.user_input['engine'] == 'gpaw':
    #         return  True
    #     else:
    #         return False

    # def user2gpaw(self)-> Dict[str, Any]:
    #     """converts general user given parameters to gpaw specific parameters."""
    #     import os
    #     parameters = self
        
    #     for key in self.user_input.keys():
    #         if key not in ['tolerance','convergance','box'] and self.user_input[key] is not None:
    #             parameters[key] = self.user_input[key]

    #         if key == 'geometry' and self.user_input[key] is None:
    #             raise ValueError('The structure file is not found')
    #     self.user_input = parameters

    def format_template(self):
        template = self.gs_template.format(**self.user_input)
        return template
     
class GpawRTLCAOTddftDelta:
    """This class contains the template  for creating gpaw 
    scripts for  real time lcao tddft calculations."""

    default_input = {'absorption_kick': [1e-5, 0.0, 0.0],
                'propagate': (20, 150),
                'module': None,
                'laser':None,
                'electric_pol': None,
                'dipole_file':'dm.dat',
                'wavefunction_file':'wf.ulm',
                'analysis_tools': None,
                'filename':'gs.gpw',
                'propagator':None,
                'td_potential': None,
                'fxc':None,
                'parallel': None,
                'txt':'tdx.out',
                'td_gpw':'td.gpw'}

    analysis_tools = [
        ('DipoleMomentWriter()','from gpaw.lcaotddft.dipolemomemtwriter import DipoleMomentWriter'),
        ('WaveFunctionWriter()','from gpaw.lcaotddft.wfwriter import WaveFunctionWriter')

    ]
    
    delta_kick_template = """ 
from gpaw.lcaotddft import LCAOTDDFT
import numpy as np
from gpaw.lcaotddft.wfwriter import WaveFunctionWriter
from gpaw.lcaotddft.dipolemomentwriter import DipoleMomentWriter

td_calc = LCAOTDDFT(filename='{filename}',txt='{txt}')

DipoleMomentWriter(td_calc, '{dipole_file}')

# Kick
td_calc.absorption_kick({absorption_kick})
# Propagate"
td_calc.propagate{propagate}
# Save the state for restarting later"
td_calc.write('{td_gpw}', mode='all')
    """


    def __init__(self, user_input) -> None:
        self.user_input = self.default_input
        self.user_input.update(user_input)
        self.tools = self.user_input['analysis_tools']

    def check():
        pass

    def get_analysis_tool():
        pass
    
    def format_template(self):

        template = self.delta_kick_template.format(**self.user_input)

        if self.tools == "dipolemoment":
            return template
        elif self.tools == "wavefunction":
            tlines = template.splitlines()
            tlines[8] = "WaveFunctionWriter(td_calc, 'wf.ulm')"
            template = """\n""".join(tlines)
            return template
       


class GpawRTLCAOTddftLaser:
    """This class contains the template  for creating gpaw 
    scripts for  real time lcao tddft calculations."""

    default_input = {
                'propagate': (20, 150),
                'module': None,
                'laser':None,
                'electric_pol': None,
                'dipole_file':'dm.dat',
                'wavefunction_file':'wf.ulm',
                'analysis_tools': None,
                'filename':'gs.gpw',
                'propagator':None,
                'td_potential': None,
                'fxc':None,
                'parallel': None,
                'txt':'tdx.out',
                'td_gpw':'td.gpw'}

    analysis_tools = [
        ('DipoleMomentWriter()','from gpaw.lcaotddft.dipolemomemtwriter import DipoleMomentWriter'),
        ('WaveFunctionWriter()','from gpaw.lcaotddft.wfwriter import WaveFunctionWriter')

    ]
    
    external_field_template = """ 
import numpy as np
from ase.units import Hartree, Bohr
from gpaw.external import ConstantElectricField
from gpaw.lcaotddft import LCAOTDDFT
from gpaw.lcaotddft.dipolemomentwriter import DipoleMomentWriter
from gpaw.lcaotddft.laser import GaussianPulse
pulse = GaussianPulse({strength},{time0}e3,{frequency},{sigma}, 'sin')
ext = ConstantElectricField(Hartree / Bohr,{electric_pol} )
td_potential = {{'ext': ext, 'laser': pulse}}
td_calc = LCAOTDDFT(filename='{filename}',
                    td_potential=td_potential,
                    txt='{txt}')
DipoleMomentWriter(td_calc, '{dipole_file}')
# Propagate"
td_calc.propagate{propagate}
# Save the state for restarting later"
td_calc.write('{td_gpw}', mode='all')
    """

    def __init__(self, user_input) -> None:
        self.user_input = self.default_input
        self.user_input.update(user_input)
        self.laser = self.user_input['laser']
        self.tools = self.user_input['analysis_tools']
        self.td_potential = self.user_input['td_potential']

    def check():
        pass
    
    def pulse(pulse_para: dict)-> str:
        para = {
            'strength':None,
            'time0':None,
            'frequency': None,
            'sigma': None,
            'sincos':'sin',
            'stoptime':'np.inf'
        }
        para.update(pulse_para)
        
        pulse = "pulse = GaussianPulse({strength},{time0},{frequency},{sigma},{sincos},{stoptime})".format(**para)
        return pulse

    def get_analysis_tool():
        pass

    def mask():
        pass
    
    def format_template(self):

        if self.laser is None:
            template = self.delta_kick_template.format(**self.user_input)

            if self.tools == "dipolemoment":
                return template
            elif self.tools == "wavefunction":
                tlines = template.splitlines()
                tlines[8] = "WaveFunctionWriter(td_calc, 'wf.ulm')"
                template = """\n""".join(tlines)
                return template

        elif self.laser is not None and self.td_potential == True:
           self.user_input.update(self.laser)
           template = self.external_field_template.format(**self.user_input)
           return template 


def write_laser(laser_input:dict, filename, directory):

    from litesoph.pre_processing.laser_design import GaussianPulse
    import numpy as np

    filename = filename + ".dat"
    filename = pathlib.Path(directory) / filename
    pulse = GaussianPulse(float(laser_input['strength']), float(laser_input['time0']),float(laser_input['frequency']), float(laser_input['sigma']), laser_input['sincos'])
    pulse.write(filename, np.arange(laser_input['range']))

class GpawSpectrum:

    default_input = {
                   'moment_file': 'dm.dat',
                   'spectrum_file': 'spec.dat',
                   'folding': 'Gauss',
                   'width' : 0.2123,
                   'e_min' : 0.0,
                   'e_max' : 30.0,
                   'delta_e' : 0.05
                }

    dm2spec="""
from gpaw.tddft.spectrum import photoabsorption_spectrum
photoabsorption_spectrum('{moment_file}', '{spectrum_file}',folding='{folding}', width={width},e_min={e_min}, e_max={e_max}, delta_e={delta_e})
"""
    
    def __init__(self, input_para: dict) -> None:
        self.dict = self.default_input
        self.dict.update(input_para)
        
    def format_template(self):
        template = self.dm2spec.format(**self.dict)
        return template


class GpawCalTCM:

    default_input = {
                    'gfilename' : 'gs.gpw',
                    'wfilename' : 'wf.ulm',
                    'frequencies' : [],
                    'name' : " "
                    }

    tcm_temp = """
from litesoph.simulations.gpaw.gpawtcm import TCMGpaw
freq = {frequencies}
ground_state = '{gfilename}'
wave_function = '{wfilename}'
tcm = TCMGpaw(ground_state, wave_function ,freq,'{name}')
tcm.run()
tcm.plot()
"""

    def __init__(self, input_para:dict) -> None:
        self.dict = self.default_input
        self.dict.update(input_para)

    def format_template(self):
        template = self.tcm_temp.format(**self.dict)
        return template


class GpawLrTddft:
    """This class contains the template  for creating gpaw 
    scripts for  linear response tddft calculations."""

    user_input = {}




class GpawInducedDensity:
    """Contains template to calculate induced density from density matrix."""
