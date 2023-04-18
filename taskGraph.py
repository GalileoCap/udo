import subprocess

class Task:
  def __init__(self, name, func):
    self.func = func

    data = func() if callable(func) else func
    if type(data) != dict:
      raise TypeError(f'Wrong type of task ({type(data)}): {data}')

    self.name = data.get('name', name)
    self.description = data.get('description', '')
    self.deps = data.get('deps', [])
    self.outs = data.get('outs', [])
    self.capture = data.get('capture', 0)
    self.actions = data.get('actions')

  def execute(self):
    print('*', self.name)
    for action in self.actions:
      if callable(action):
        action()
      elif type(action) == str:
        res = subprocess.run(
          action, shell = True,
          stdout = subprocess.PIPE if self.capture < 1 else None,
          stderr = subprocess.PIPE if self.capture < 0 else None,
        )
        res.check_returncode()
      else:
        raise TypeError(f'\tWrong type of action ({type(action)}): {action}')

  #************************************************************
  #* Utils ****************************************************
  def __repr__(self):
    name = self.name
    description = self.description
    deps = self.deps
    outs = self.outs
    capture = self.capture
    actions = self.actions
    return f'Task<{name},{description},{deps=},{outs=},{capture=},{actions=}>'
  def __str__(self):
    return self.__repr__()

class TaskGraph:
  def __init__(self, tasks):
    self.tasks = tasks

  def execute(self):
    #TODO: Change to pseudo-dfs to make it easier to follow
    for task in self.tasks:
      task.visited = 0
    queue = [task for task in self.tasks if len(task.parents) == 0]

    while len(queue) != 0:
      task = queue.pop(0)
      task.execute()

      for child in task.children:
        child.visited += 1
        if child.visited == len(child.parents):
          queue.append(child)

  def check(self):
    emptyTasks = self.checkEmpty()
    if len(emptyTasks) != 0:
      raise Exception(f'Empty tasks: {emptyTasks}')

    multipleProducers = self.checkMultipleProducers()
    if len(multipleProducers) != 0:
      raise Exception(f'Repeated tags {multipleProducers}')

    if self.checkLoops():
      raise Exception('Loop found')

  def calcEdges(self):
    for task in self.tasks:
      task.parents = []
      task.children = []

    for task in self.tasks:
      for dep in task.deps:
        parent = self.getNodeByDep(dep)
        if parent is None:
          raise Exception(f'No task matches dependency: {dep}, for task: {task.name}')

        task.parents.append(parent)
        parent.children.append(task)

  #************************************************************
  #* Checks ***************************************************
  def checkEmpty(self):
    res = []
    for task in self.tasks:
      if len([action for action in task.actions if action != '']) == 0:
        res.append(task)
    return res

  def checkMultipleProducers(self):
    counts = {} #TODO: Rename
    for task in self.tasks:
      for tag in task.outs:
        counts[tag] = counts.get(tag, []) + [task.name]
    return [(tag, count) for tag, count in counts.items() if len(count) > 1]

  def checkLoops(self):
    for task in self.tasks:
      task.visited = 0

    cnt = 0
    queue = [task for task in self.tasks if len(task.parents) == 0]
    while len(queue) != 0:
      task = queue.pop(0)
      for child in task.children:
        child.visited += 1
        if child.visited == len(child.parents):
          queue.append(child)
      cnt += 1

    #TODO: Detect exactly which loops are there
    return cnt != len(self.tasks)

  #************************************************************
  #* Utils ****************************************************
  def getNodeByDep(self, dep):
    for task in self.tasks:
      if (
        ((callable(dep) or type(dep) == dict) and dep == task.func) or
        (type(dep) == str and dep in task.outs)
      ):
        return task
    return None
