from importlib import import_module
import argparse

def importFile(fpath):
  return import_module(fpath[:-3])

def parseArgs():
  parser = argparse.ArgumentParser(
    prog = 'udo',
    description = 'Task executer', #TODO: Better description
    #TODO: Other parameters
  )

  parser.add_argument('targets')
  parser.add_argument('-f', '--file', default = 'udo.py')
  #TODO: Docs

  return parser.parse_args()
