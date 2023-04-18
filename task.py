import subprocess

import utils

class Task:
  def __init__(self, name, func):
    self.func = func

    data = func() if callable(func) else func
    if type(data) != dict:
      print('Wrong type:', type(data), data)
      #TODO: Error

    self.name = data.get('name', name)
    self.description = data.get('description', '')
    self.dependsOn = data.get('dependsOn', [])
    self.produces = data.get('produces', [])
    self.capture = data.get('capture', [])
    self.actions = data.get('actions')

    self.parents = []
    self.children = []

    self.loop_visited = 0
    self.exec_visited = 0

  def exec(self):
    for action in self.actions:
      if callable(action):
        action()
      elif type(action) == str:
        res = subprocess.run(action, shell = True, capture_output = True)
        res.check_returncode()
        print(res.stdout, res.stderr)
      else:
        print('ERROR')

  def __repr__(self):
    name = self.name
    description = self.description
    dependsOn = self.dependsOn
    produces = self.produces
    capture = self.capture
    actions = self.actions
    return f'Task<{name},{description},{dependsOn=},{produces=},{capture=},{actions=}>'
  def __str__(self):
    return self.__repr__()

def loadTasks(mod):
  return [
    Task(name, func)
    for name, func in mod.__dict__.items()
    if name.startswith('Task') and (callable(func) or type(func) == dict)
  ]

def getTaskByFunc(tasks, func):
  for task in tasks:
    if func == task.func:
      return task

def getTaskByProduce(tasks, file):
  for task in tasks:
    if file in task.produces:
      return task

def buildTaskGraph(tasks):
  for task in tasks:
    for dep in task.dependsOn:
      parent = None
      if callable(dep):
        parent = getTaskByFunc(tasks, dep)
      else:
        parent = getTaskByProduce(tasks, dep)

      if parent is None:
        print('none parent')
        #TODO: Error

      task.parents.append(parent)
      parent.children.append(task)

def checkMultipleProducers(tasks):
  produces = set()
  for task in tasks:
    for out in task.produces:
      if out in produces:
        return True
      produces.add(out)

def checkEmpty(tasks):
  for task in tasks:
    if len([action for action in task.actions if action != '']) == 0:
      return True

def checkLoops(tasks):
  queue = [task for task in tasks if len(task.parents) == 0]

  cnt = 0
  while len(queue) != 0:
    task = queue.pop(0)
    for child in task.children:
      child.loop_visited += 1
      if child.loop_visited == len(child.parents):
        queue.append(child)
    cnt += 1

  return cnt != len(tasks)

def checkTaskGraph(tasks):
  return checkMultipleProducers(tasks) or checkEmpty(tasks) or checkLoops(tasks)

def getTaskGraph(tasks):
  buildTaskGraph(tasks)

  if checkTaskGraph(tasks):
    #TODO: Error and log cause
    print('Error')

  return tasks
