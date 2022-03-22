
import os 
import subprocess
import pathlib
from configparser import ConfigParser

import litesoph


config_file = pathlib.Path.home() / "lsconfig.ini"

lsroot = pathlib.Path(litesoph.__file__).parent.parent


sections = {
    'visualization_tools' : ['vmd', 'vesta'],
    'engine' : ['gpaw','nwchem','octopus'],
    'programs' : ['python'],
    'mpi' : ['mpirun'],
}


def get_path(name):
    print("Checking for {}....".format(name))
    p = subprocess.run(['which', name], capture_output=True, text=True)
    if p.stdout and p.returncode == 0:
        print("Found {} in {}".format(name, p.stdout.split()[0]))
        return p.stdout.split()[0]
    else:
        print("Did not find {}".format(name))
        return None
    

def create_default_config(config: ConfigParser, sections: dict):
    for key, valve in sections.items():
        config.add_section(key)
        for option in valve:
            set = get_path(option)
            if set is not None:
                config.set(key, option, set)
            else:
                config.set(key, option , '')

def write_config():
    config = ConfigParser(allow_no_value=True)
    config.add_section('path')
    config.set('path','lsproject', str(pathlib.Path.home()))
    print(f"setting lsroot:{str(lsroot)}")
    config.set('path','lsroot',str(lsroot))
    create_default_config(config, sections)

    config.set('mpi', 'gpaw_mpi', '')
    config.set('mpi', 'octopus_mpi', '')
    config.set('mpi', 'nwchem_mpi', '')

    print('Creating ~/lsconfig.ini ...')
    try:
        with open(config_file, 'w+') as configfile:
            config.write(configfile)
    except Exception as e:
        raise e
    else:
        print('Done.')


def check_config(lsconfig: ConfigParser, name):
    if name == "lsroot":
        try:
            lsroot = pathlib.Path(lsconfig.get("path", "lsroot" ))
        except:
            print("Please set lsroot in ~/lsconfig.ini")
            exit()
        else:
            return lsroot
    if name == "vis":
        try:
           vis_tool = list(lsconfig.items("visualization_tools"))[0][1]
        except:
            print("Please set path to vmd or vesta in ~/lsconfig.ini and first one will be used")
        else:
            return vis_tool
        # try:
        #     vmd = lsconfig.get("visualization_tools", "vmd" )
        # try:
        #     vmd = lsconfig.get("visualization_tools", "vesta" )
        # except:
        #     print("Please set path to vmd in ~/lsconfig.ini")
        # else:
        #     return vmd