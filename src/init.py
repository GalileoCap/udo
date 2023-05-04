from utils import currVersion

def initFile():
  s = '# Default uDO file\n'

  s += '''
UDOConfig = {
  'version': ''' + f"'{currVersion}'" + '''
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
