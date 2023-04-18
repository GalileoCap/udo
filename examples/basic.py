FPATH = '/tmp/test.touch'

def TaskTouch():
  return {
    'description': 'Creates the file',

    'outs': [FPATH], # This task creates these files

    'actions': [
      f'echo "Ahoy there!" > {FPATH}',
    ],
  }

def TaskMessage():
  return {
    'description': 'Prints the file',

    'deps': [FPATH], # This task depends on these files
    'capture': 1, # Show stdout

    'actions': [
      f'cat {FPATH}',
    ],
  }
