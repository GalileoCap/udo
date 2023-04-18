import subprocess

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
    self.capture = data.get('capture', 0)
    self.actions = data.get('actions')

  def execute(self):
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
      print('Empty tasks:', emptyTasks)
      return False

    multipleProducers = self.checkMultipleProducers()
    if len(multipleProducers) != 0:
      print('Repeated tags:', multipleProducers)
      return False

    return not self.checkLoops()

    return True

  def calcEdges(self):
    for task in self.tasks:
      task.parents = []
      task.children = []

    for task in self.tasks:
      for dep in task.dependsOn:
        parent = self.getNodeByDep(dep)
        if parent is None:
          print('none parent')
          #TODO: Error

        task.parents.append(parent)
        parent.children.append(task)

  def checkEmpty(self):
    res = []
    for task in self.tasks:
      if len([action for action in task.actions if action != '']) == 0:
        res.append(task)
    return res

  def checkMultipleProducers(self):
    counts = {} #TODO: Rename
    for task in self.tasks:
      for tag in task.produces:
        counts[tag] = counts.get(tag, []) + [task]
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

  def getNodeByDep(self, dep):
    for task in self.tasks:
      if (
        ((callable(dep) or type(dep) == dict) and dep == task.func) or
        (type(dep) == str and dep in task.produces)
      ):
        return task
    return None
