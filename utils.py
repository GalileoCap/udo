from importlib import import_module
import argparse

from taskGraph import Task

def loadTasks(fpath):
  mod = import_module(fpath[:-3])
  return [
    Task(name, func)
    for name, func in mod.__dict__.items()
    if name.startswith('Task') and (callable(func) or type(func) == dict)
  ]

def parseArgs():
  parser = argparse.ArgumentParser(
    prog = 'udo',
    description = 'Task executer', #TODO: Better description
    #TODO: Other parameters
  )

  parser.add_argument('targets', default = '')
  parser.add_argument('-f', '--file', default = 'udo.py')
  #TODO: Docs

  return parser.parse_args()
