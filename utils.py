import argparse
import hashlib
import os

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

def hashFile(fpath):
  #SEE: https://stackoverflow.com/a/3431838
  if os.path.isdir(fpath): #TODO: Hash directories based on recursive hashes
    return os.path.exists(fpath)

  md5 = hashlib.md5()
  with open(fpath, 'rb') as fin:
    for chunk in iter(lambda: fin.read(1024 * 4), b''):
      md5.update(chunk)
  return md5.digest()
