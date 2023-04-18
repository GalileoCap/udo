FPATH = '/tmp/test.touch'

def TaskTouch():
  return {
    'name': 'Touch',
    'description': 'Creates the file',

    'outs': [FPATH],

    'capture': 1, # Show stdout
    'actions': [
      f'echo "Ahoy there!" > {FPATH}',
      f'cat {FPATH}',
    ],
  }

def TaskRemoveTouch():
  return {
    'description': 'Deletes the file',
    'deps': [FPATH],

    'actions': [
      f'rm {FPATH}',
    ],
  }
