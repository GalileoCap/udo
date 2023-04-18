FPATH = '/tmp/test.touch'

def TaskTouch():
  return {
    'name': 'Touch',
    'description': 'Creates the file',

    'dependsOn': [],
    'produces': [FPATH],

    'actions': [
      f'echo "Ahoy there" > {FPATH}',
    ],
  }

TaskRemoveTouch = {
  'name': 'RemoveTouch',
  'dependsOn': [FPATH],

  'actions': [
    f'rm {FPATH}',
  ],
}

msgCount = 0
def printMsg():
  msgCount += 1
  print(f'The message has been called: {msgCount} times')

def TaskLoopA():
  return {
    'name': 'LoopA',
    'dependsOn': [TaskLoopB],

    'capture': 1,
    'actions': [
      printMsg
    ],
  }

def TaskLoopB():
  return {
    'name': 'LoopB',
    'dependsOn': [TaskLoopB],

    'capture': 1,
    'actions': [
      printMsg
    ],
  }
