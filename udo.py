FPATH = '/tmp/test.touch'

def TaskTouch():
  return {
    'name': 'Touch',
    'description': 'Creates the file',

    'dependsOn': [],
    'produces': [FPATH],

    'capture': 1,
    'actions': [
      f'echo "Ahoy there!" > {FPATH}',
      f'cat {FPATH}',
    ],
  }

TaskRemoveTouch = {
  'name': 'RemoveTouch',
  'dependsOn': [FPATH],

  'actions': [
    f'rm {FPATH}',
  ],
}

def printMsg():
  print('Ahoy my friend!')

TaskMsg = {
  'name': 'Msg',

  'capture': 1,
  'actions': [
    printMsg
  ],
}
