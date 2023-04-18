import utils

class Task:
  def __init__(self, *,
      name, description = '',
      dependsOn = [], produces = [],
      capture = 0,
      actions = [],
    ):
    self.name = name
    self.description = description
    self.dependsOn = dependsOn
    self.produces = produces
    self.capture = capture
    self.actions = actions

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

def getTasks(mod):
  tasks = []

  for func in (
    func
    for name, func in mod.__dict__.items()
    if name.startswith('Task') and (callable(func) or type(func) == dict)
  ):
    data = func() if callable(func) else func
    if type(data) != dict:
      print('Wrong type:', type(data), data)
      continue
    tasks.append(Task(**data))

  return tasks
