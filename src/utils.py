import argparse
import hashlib
from shutil import rmtree
import os

def parseArgs():
  parser = argparse.ArgumentParser(
    prog = 'udo',
    description = 'Task executer', #TODO: Better description
    #TODO: Other parameters
  )

  parser.add_argument('targets', nargs = '*', default = '')
  parser.add_argument('-f', '--file', default = 'udo.py')
  parser.add_argument('--cachePath', default = '.udo.db')
  #TODO: Docs

  return parser.parse_args()

def hashFile(fpath):
  #SEE: https://stackoverflow.com/a/3431838
  if os.path.isdir(fpath): #TODO: Hash directories based on recursive hashes
    return os.path.exists(fpath)

  md5 = hashlib.md5()
  with open(fpath, 'rb') as fin:
    for chunk in iter(lambda: fin.read(1024 * 4), b''):
      md5.update(chunk)
  return md5.digest()

def cleanTasks(tasks):
  #TODO: Traverse graph to clean
  for task in tasks:
    if not task.isSubtask:
      print(f'  * {task.name}')
    if task.clean:
      for out in task.outs:
        if os.path.isdir(out): rmtree(out)
        elif os.path.isfile(out): os.remove(out)

def printHelp(tasks):
  for task in tasks:
    if not task.isSubtask:
      print(f'  * {task.name}{":" if task.description != "" else ""} {task.description}')
