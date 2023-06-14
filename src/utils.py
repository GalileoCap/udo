from importlib import import_module
import importlib.util
import argparse
import hashlib
from shutil import rmtree
import os

currVersion = (1, 4, 0)

dfltFile = './udo.py'
dfltCache = './.udo.db'
dfltPrefix = 'Task'
dfltForce = ''
dfltForceAll = False
dfltInit = False

def parseArgs():
  major, minor, patch = currVersion

  parser = argparse.ArgumentParser(
    prog = f'udo',
    description = f'v{major}.{minor}.{patch}', #TODO: Better description
    epilog = 'Made by Galileo Cappella\nVisit https://dev.galileocap.me/udo',

    formatter_class = argparse.RawTextHelpFormatter,
  )

  parser.add_argument(
    'targets', nargs = '*', default = [],
    help = 'List of targets to be executed. Defaults to all if empty.\nUse target "help" to list possible targets.'
  )
  parser.add_argument(
    '--file', default = dfltFile,
    help = f'Path to the file describing the tasks (default: "{dfltFile}")',
  )
  parser.add_argument(
    '--cache', default = None,
    help = f'Path to the file where the cache is stored and read (default: "{dfltCache}")',
  )
  parser.add_argument(
    '--prefix', default = None,
    help = f'Prefix used to look for tasks (default: "{dfltPrefix}")',
  )
  parser.add_argument(
    '--force', default = dfltForce,
    help = f'Comma separated list (no spaces) of tasks to force their execution, skipping checks (default: {dfltForce})',
  )
  parser.add_argument(
    '--forceAll', default = None, action = 'store_true',
    help = f'Force the execution of all targets (default: {dfltForceAll})',
  )
  parser.add_argument(
    '--init', default = dfltInit, action = 'store_true',
    help = f'Creates a basic configuration file (uses --file) (default: {dfltInit})',
  )

  return parser.parse_args()

def loadModule(fpath):
  # SEE: https://stackoverflow.com/a/67692
  modName = fpath[:-3]
  spec = importlib.util.spec_from_file_location(modName, os.path.join(os.getcwd(), fpath))
  mod = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(mod)
  return mod

def hashFile(fpath):
  #SEE: https://stackoverflow.com/a/3431838
  if os.path.isdir(fpath): #TODO: Hash directories based on recursive hashes
    return os.path.exists(fpath)

  md5 = hashlib.md5()
  with open(fpath, 'rb') as fin:
    for chunk in iter(lambda: fin.read(1024 * 4), b''):
      md5.update(chunk)
  return md5.digest()

def printHelp(tasks):
  for task in tasks:
    if not task.isSubtask:
      print(f'  * {task.name}{":" if task.description != "" else ""} {task.description}')
