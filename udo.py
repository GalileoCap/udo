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

msgCount = 0
def printMsg():
  global msgCount
  msgCount += 1
  print(f'Ahoy my friend!... For the {msgCount}st,nd,rd,th time')

TaskMsg = {
  'name': 'Msg',

  'capture': 1,
  'actions': [
    printMsg
  ],
}

# def TaskLoopA():
  # return {
    # 'name': 'LoopA',
    # 'dependsOn': [TaskLoopC],
    # 'actions': [printMsg],
  # }
#
# TaskLoopB = {
  # 'name': 'LoopB',
  # 'dependsOn': [TaskLoopA],
  # 'actions': [printMsg],
# }
#
# TaskLoopC = {
  # 'name': 'LoopC',
  # 'dependsOn': [TaskLoopB],
  # 'actions': [printMsg],
# }
