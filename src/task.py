import subprocess
import os
import inspect
import shutil

from cache import getCache, setCache
from config import config
from utils import hashFile

class Task:
  def __init__(self, name, func, *, namePrefix = '', isSubtask = False):
    self.func = func

    data = func() if callable(func) else func
    if type(data) != dict:
      raise TypeError(f'Wrong type of task ({type(data)}): {data}')

    self.name = namePrefix + data.get('name', name.lstrip('Task'))
    self.description = data.get('description', '')
    self.deps = data.get('deps', [])
    self.outs = data.get('outs', [])
    self.clean = data.get('clean', True)
    self.skipRun = data.get('skipRun', self.checkCache)
    self.capture = data.get('capture', 0)
    self.cache = getCache(self.name)
    self.isSubtask = isSubtask
    self.retCode = 0

    self.actions = data.get('actions', [])
    self.subtasks = []
    for subfunc in data.get('subtasks', []):
      subtask = Task('', subfunc, namePrefix = f'{self.name}:', isSubtask = True)
      self.deps.append(subtask.func)
      self.subtasks.append(subtask)

    if 'name' == '':
      raise Exception(f'Task must have a name: {data}')
    
  #************************************************************
  #* Execution ************************************************

  def execute(self, mode):
    if mode == 'exec': return self.exec()
    elif mode == 'help': return self.execHelp()
    elif mode == 'clean': return self.execClean()

  def exec(self):
    if not (self.name in config['force'] or config['forceAll']) and self.shouldSkipRun():
      print('-', self.name)
      return self.retCode == 0
    
    print('+', self.name)
    for action in self.actions:
      if callable(action):
        action()
      elif type(action) == str:
        res = subprocess.run(
          action, shell = True,
          stdout = subprocess.PIPE if self.capture < 1 else None,
          stderr = subprocess.PIPE if self.capture < 0 else None,
        )

        self.retCode = res.returncode
        if self.retCode != 0:
          return False
      else:
        raise TypeError(f'\tWrong type of action ({type(action)}): {action}')

    missingOuts = self.checkOuts()
    if len(missingOuts) != 0:
      raise Exception(f'\tNot all outs were created: {missingOuts}')
    self.cacheOuts()
    return True

  def execHelp(self):
    if not self.isSubtask:
      print(f'* {self.name}' + (f': {self.description}' if self.description != '' else ''))
    return True

  def execClean(self):
    # TODO: In the documentation clean was explained as only being used to check whether to delete files, but in practice if it was callable it was called INSTEAD of deleting outs. This implementation currently follows the previous functionality but should be split into skipClean and clean.
    # TODO: Always return True?
    if not self.clean:
      print('-', self.name) # TODO: Repeated code
      return True

    print('+', self.name)
    if callable(self.clean): self.clean()
    else:
      for out in self.outs:
        if os.path.isdir(out): shutil.rmtree(out)
        elif os.path.isfile(out): os.remove(out)
    return True

  #************************************************************
  #* Cache ****************************************************

  def shouldSkipRun(self):
    skipRun = self.skipRun() if callable(self.skipRun) else self.skipRun
    return skipRun or len(self.actions) == 0

  def checkCache(self):
    cacheOuts = self.cache.get('outs', [])
    cacheDeps = self.cache.get('deps', [])
    cacheActions = self.cache.get('actions', [])
    hasCache = len(cacheOuts) != 0 or len(cacheDeps) != 0 or len(cacheActions) != 0
    return hasCache and self.cache == self.calcCache()

  def checkOuts(self):
    return [
      out
      for out in self.outs
      if type(out) == str and not os.path.exists(out)
    ]

  def cacheOuts(self):
    self.cache = self.calcCache()
    setCache(self.name, self.cache)

  #************************************************************
  #* Utils ****************************************************

  def calcCache(self):
    return {
      'deps': self.calcCacheDeps(),
      'outs': self.calcCacheOuts(),
      'actions': self.calcCacheActions(),
    }

  def calcCacheDeps(self): 
    return {
      dep: hashFile(dep) if os.path.exists(dep) else ''
      for dep in self.deps 
      if type(dep) == str
    }

  def calcCacheOuts(self):
    return {
      out: hashFile(out) if os.path.exists(out) else ''
      for out in self.outs
      if type(out) == str
    }

  def calcCacheActions(self):
    return [
      inspect.getsource(action) if callable(action) else action
      for action in self.actions
    ]

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

class InternalTask(Task) :
  def __init__(self, name, func, *, namePrefix = '', isSubtask = False):
    super().__init__(name, func, namePrefix = namePrefix, isSubtask = isSubtask)

  def calcCacheActions(self):
    # NOTE: Fixes not being able to inspect.getsource on functions defined in this module
    return [
      action
      for action in self.actions
      if not callable(action) # TODO: What to do with callables?
    ]

def loadTasks(mod):
  tasks = []
  for name, func in mod.__dict__.items():
    if name.startswith(config['prefix']) and (callable(func) or type(func) == dict):
      task = Task(name, func)
      tasks.append(task)
      tasks.extend(task.subtasks)

  return tasks
