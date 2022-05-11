from configparser import ConfigParser
import pathlib
import re

from litesoph.simulations.engine import EngineStrategy,EngineGpaw,EngineNwchem,EngineOctopus

def get_engine_obj(engine, *args, **kwargs)-> EngineStrategy:
    """ It takes engine name and returns coresponding EngineStrategy class"""

    if engine == 'gpaw':
        return EngineGpaw(*args, **kwargs)
    elif engine == 'octopus':
        return  EngineOctopus(*args, **kwargs)
    elif engine == 'nwchem':
        return EngineNwchem(*args, **kwargs)

class Task:

    """It takes in the user input dictionary as input."""

    BASH_filename = 'job_script.sh'

    def __init__(self, engine_name, status, project_dir:pathlib.Path, lsconfig:ConfigParser) -> None:
        
        self.status = status
        self.lsconfig = lsconfig
       
        self.project_dir = project_dir
        self.task_dir = None
        self.task = None
        self.filename = None
        self.template = None
        self.input_data_files = []
        self.output_data_file = []
        self.task_state = None

        self.engine_name = engine_name
        self.engine = get_engine_obj(self.engine_name, project_dir = self.project_dir, lsconfig = self.lsconfig, status=self.status)
        self.prepend_project_name()

    def prepend_project_name(self):

        self.filename = pathlib.Path(f"{self.project_dir.name}/{self.task_data['inp']}")
        for item in self.task_data['req']:
            item = pathlib.Path(self.project_dir.name) / item
            self.input_data_files.append(item)
        try:
            self.output_log_file =   pathlib.Path(f"{self.project_dir.name}/{self.task_data['out_log']}")
        except KeyError:
            pass
        
    def create_template(self):
        ...
       
    def write_input(self, template=None):
        
        if template:
            self.template = template
        if not self.task_dir:
            self.create_task_dir()
        if not self.template:
            msg = 'Template not given or created'
            raise Exception(msg)
        self.engine.create_script(self.task_dir, self.template, self.filename.name)

    def check_prerequisite(self, network=False) -> bool:
        """ checks if the input files and required data files for the present task are present"""
        
        inupt_file = self.project_dir.parent / self.filename
        
        if not pathlib.Path(inupt_file).exists():
            check = False
            msg = f"Input file:{inupt_file} not found."
            raise FileNotFoundError(msg)

        if network:
            if not  self.bash_file.exists():
                msg = f"job_script:{ self.bash_file} not found."
                raise FileNotFoundError(msg)
            self.bash_filename =  self.bash_file.relative_to(self.project_dir.parent)
            return
            
        for item in self.input_data_files:
            item = self.project_dir.parent / item
            if not pathlib.Path(item).exists():
                msg = f"Data file:{item} not found."
                raise FileNotFoundError(msg)
    
    def create_remote_job_script(self, np) -> str:
        """Create the bash script to run the job and "touch Done" command to it, to know when the 
        command is completed."""
        try:
            job_script = self.engine.get_engine_network_job_cmd()
        except AttributeError:
            job_script = ''
         
        job_script += self.get_network_job_cmd(np)
        job_script += "touch Done\n"
        job_script += "##############################"
        return job_script

    def write_remote_job_script(self, job_script):
        self.bash_file = self.project_dir / self.BASH_filename
        with open(self.bash_file, 'w+') as f:
            f.write(job_script)

    def create_task_dir(self):
        self.task_dir = self.engine.create_dir(self.project_dir, type(self).__name__)

    def replacetext(filename, search_text,replace_text):

        with open(filename,'r+') as f:
            file = f.read()
            file = re.sub(search_text, replace_text, file)
            f.seek(0)
            f.write(file)
            f.truncate()

    def set_submit_local(self, *args):
        from litesoph.utilities.job_submit import SubmitLocal
        
        self.sumbit_local = SubmitLocal(self, *args)

    def run_job_local(self):        
        self.sumbit_local.prepare_input()
        self.sumbit_local.run_job()
        
def pbs_job_script(name):

    head_job_script = f"""
#!/bin/bash
#PBS -N {name}
#PBS -o output.txt
#PBS -e error.txt
#PBS -l select=1:ncpus=4:mpiprocs=4
#PBS -q debug
#PBS -l walltime=00:30:00
#PBS -V
cd $PBS_O_WORKDIR
   """
    return head_job_script






  

