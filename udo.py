FPATH = '/tmp/test.touch'

def TaskTouch():
  return {
    'name': 'Touch',
    'description': 'Creates the file',

    'deps': [],
    'outs': [FPATH],

    'capture': 1,
    'actions': [
      f'echo "Ahoy there!" > {FPATH}',
      f'cat {FPATH}',
    ],
  }

TaskRemoveTouch = {
  'deps': [FPATH],

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
  'capture': 1,
  'actions': [
    printMsg
  ],
}

# def TaskLoopA():
  # return {
    # 'name': 'LoopA',
    # 'deps': [TaskLoopC],
    # 'actions': [printMsg],
  # }
#
# TaskLoopB = {
  # 'name': 'LoopB',
  # 'deps': [TaskLoopA],
  # 'actions': [printMsg],
# }
#
# TaskLoopC = {
  # 'name': 'LoopC',
  # 'deps': [TaskLoopB],
  # 'actions': [printMsg],
# }
