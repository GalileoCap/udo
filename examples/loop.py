def printMsg():
  print('Ahoy there!')

def TaskLoopA():
  return {
    'name': 'LoopA',
    'deps': [TaskLoopC],
    'actions': [printMsg],
  }

def TaskLoopB():
  return {
    'name': 'LoopB',
    'deps': [TaskLoopA],
    'actions': [printMsg],
  }

def TaskLoopC():
  return {
    'name': 'LoopC',
    'deps': [TaskLoopB],
    'actions': [printMsg],
  }
