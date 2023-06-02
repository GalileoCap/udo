import os

from config import config
from utils import currVersion

def initFile():
  major, minor, patch = currVersion

  s = '# Default uDO file\n'

  s += '''
UDOConfig = {
  'version': ''' + f'({major}, {minor}, {patch})' + '''
}
'''

  s += '''
def TaskMain():
  return {
    'name': 'main',
    'capture': 1,

    'actions': [
      'echo -n Hello',
      lambda: print(' World'),
    ],
  }

def TaskShamelessPlug():
  return {
    'deps': [TaskMain],
    'actions': [
      lambda: print('For more help visit: https://dev.galileocap.me/udo')
    ],
  }
'''

  return s

def doInit(filePath):
  print(f'Creating default configuration at: {filePath}')
  with open(filePath, 'w') as fout:
    fout.write(initFile())

  if os.path.isfile('.gitignore'):
    print(f'.gitignore found, appending {config["cache"]}')
    with open('.gitignore', 'a') as fout:
      fout.write(f'\n{config["cache"]}\n')
