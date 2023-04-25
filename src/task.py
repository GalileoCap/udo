import subprocess
import os

from cache import getCache, setCache
from utils import hashFile, printHelp, cleanTasks

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

    self.actions = data.get('actions', [])
    self.subtasks = []
    for subfunc in data.get('subtasks', []):
      subtask = Task('', subfunc, namePrefix = f'{self.name}:', isSubtask = True)
      self.deps.append(subtask.func)
      self.subtasks.append(subtask)

    if 'name' == '':
      raise Exception(f'Task must have a name: {data}')

  def execute(self):
    if self.shouldSkipRun():
      print('-', self.name)
      return
    
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
        res.check_returncode()
      else:
        raise TypeError(f'\tWrong type of action ({type(action)}): {action}')

    missingOuts = self.checkOuts()
    if len(missingOuts) != 0:
      raise Exception(f'\tNot all outs were created: {missingOuts}')
    self.cacheOuts()

  def shouldSkipRun(self):
    skipRun = self.skipRun() if callable(self.skipRun) else self.skipRun
    return skipRun or len(self.actions) == 0

  def checkCache(self):
    cacheOuts = self.cache.get('outs', [])
    cacheDeps = self.cache.get('deps', [])
    hasCache = len(cacheOuts) != 0 or len(cacheDeps) != 0
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
      'deps': {
        dep: hashFile(dep) if os.path.exists(dep) else ''
        for dep in self.deps 
        if type(dep) == str
      },
      'outs': {
        out: hashFile(out) if os.path.exists(out) else ''
        for out in self.outs
        if type(out) == str
      },
    }

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

def loadTasks(mod):
  tasks = []
  for name, func in mod.__dict__.items():
    if name.startswith('Task') and (callable(func) or type(func) == dict):
      task = Task(name, func)
      tasks.append(task)
      tasks.extend(task.subtasks)

  return tasks

def TaskClean(tasks):
  return Task('clean', {
    'description': 'Removes all outs created by other tasks that have the "clean" attribute set as True',
    'capture': 1,
    'actions': [lambda: cleanTasks(tasks)],
  })

def TaskHelp(tasks):
  return Task('help', {
    'description': 'Prints this message',
    'actions': [lambda: printHelp(tasks)],
  })
