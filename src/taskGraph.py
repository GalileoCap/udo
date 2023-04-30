from task import TaskClean, TaskHelp

class TaskGraph:
  class Node:
    def __init__(self, task):
      self.task = task
      self.parents = []
      self.children = []

    def execute(self):
      if self.visited:
        return
        
      self.visited = True
      for parent in self.parents:
        parent.execute()
      self.task.execute()

    def getRoots(self):
      if len(self.parents) == 0:
        return [self]

      roots = []
      for parent in self.parents:
        roots += parent.getRoots()
      return roots

    def getLeaves(self):
      #TODO: Repeated code from getRoots
      if len(self.children) == 0:
        return [self]

      leaves = []
      for child in self.children:
        leaves += child.getLeaves()
      return leaves
  
    def __repr__(self):
      return f'Node<{self.task.__repr__()},parents={len(self.parents)},children={len(self.children)}>'
    def __str__(self):
      return self.__repr__()

  def __init__(self, tasks):
    self.tasks = tasks
    self.nodes = [self.Node(task) for task in tasks]

  def execute(self, targets):
    if targets == ['clean']: TaskClean(self.tasks).execute()
    elif targets == ['help']: TaskHelp(self.tasks).execute()
    else:
      leaves = self.getLeaves(targets)

      for node in self.nodes:
        node.visited = False
      for node in leaves:
        node.execute()

  def check(self):
    # emptyTasks = self.checkEmpty()
    # if len(emptyTasks) != 0:
      # raise Exception(f'Empty tasks: {emptyTasks}')

    multipleProducers = self.checkMultipleProducers()
    if len(multipleProducers) != 0:
      raise Exception(f'Repeated tags {multipleProducers}')

    if self.checkLoops():
      raise Exception('Loop found')

  def calcEdges(self):
    for node in self.nodes:
      for dep in node.task.deps:
        parent = self.getNodeByDep(dep)
        if not parent is None:
          node.parents.append(parent)
          parent.children.append(node)

  #************************************************************
  #* Checks ***************************************************
  def checkEmpty(self):
    res = []
    for node in self.nodes:
      if len([action for action in node.task.actions if action != '']) == 0:
        res.append(node.task)
    return res

  def checkMultipleProducers(self):
    #TODO: Clean
    counts = {} #TODO: Rename
    for node in self.nodes:
      for tag in node.task.outs:
        counts[tag] = counts.get(tag, []) + [node.task.name]
    return [(tag, count) for tag, count in counts.items() if len(count) > 1]

  def checkLoops(self):
    for node in self.nodes:
      node.visited = 0

    cnt = 0
    queue = self.getRoots()
    while len(queue) != 0:
      node = queue.pop(0)
      for child in node.children:
        child.visited += 1
        if child.visited == len(child.parents):
          queue.append(child)
      cnt += 1

    #TODO: Detect exactly which loops are there
    return cnt != len(self.nodes)

  #************************************************************
  #* Utils ****************************************************
  def getRoots(self, targets = []):
    if len(targets) == 0:
      return [node for node in self.nodes if len(node.parents) == 0]
    else:
      roots = []
      for target in targets:
        roots += self.getNodeByName(target).getRoots()
      return list(set(roots)) # Remove repeats

  def getLeaves(self, targets = []):
    #TODO: Repeated code with getRoots
    if len(targets) == 0:
      return [node for node in self.nodes if len(node.children) == 0]
    else:
      leaves = []
      for target in targets:
        leaves += [self.getNodeByName(target)]
      return list(set(leaves)) # Remove repeats

  def getNodeByName(self, name):
    for node in self.nodes:
      if node.task.name == name:
        return node
    return None

  def getNodeByDep(self, dep):
    for node in self.nodes:
      if (
        ((callable(dep) or type(dep) == dict) and dep == node.task.func) or
        (type(dep) == str and dep in node.task.outs)
      ):
        return node
    return None
