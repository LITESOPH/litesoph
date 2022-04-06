import subprocess
import os 
import pathlib

import litesoph

lsroot = litesoph.pre_processing.__file__
lsroot = pathlib.Path(lsroot) 
lsroot = lsroot.parent

Tools=[]

class Runner:
    
    def __init__(self) -> None:
        pass

    def parse(self, args):
        print(args)

class CLICommand:
    """Run Pre Processing Tools.

    """

    @staticmethod
    def add_arguments(parser):
        add = parser.add_argument
        add('Tool', nargs='?', default='',
            help='which tool to run')
        add('-p', '--parameters', default='',
            metavar='key=value,...',
            help='Comma-separated key=value pairs of ' +
            'tools specific parameters.')

    @staticmethod
    def run(args):
        runner = Runner()
        runner.parse(args)

        
       
        