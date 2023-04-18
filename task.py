from importlib import import_module
import subprocess
import os

from cache import getCache, setCache
from utils import hashFile, printHelp, cleanTasks

class Task:
  def __init__(self, name, func):
    self.func = func

    data = func() if callable(func) else func
    if type(data) != dict:
      raise TypeError(f'Wrong type of task ({type(data)}): {data}')

    self.name = data.get('name', name.lstrip('Task'))
    self.description = data.get('description', '')
    self.deps = data.get('deps', [])
    self.outs = data.get('outs', [])
    self.capture = data.get('capture', 0)
    self.actions = data.get('actions')
    
    self.cache = getCache(self.name)

  def execute(self):
    skipRun = self.checkCache()
    if skipRun:
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

  def checkCache(self):
    return len(self.cache) != 0 and self.cache == self.calcCache()

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
      out: hashFile(out) if os.path.exists(out) else ''
      for out in self.outs
      if type(out) == str
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

def loadTasks(fpath):
  mod = import_module(fpath[:-3])
  tasks = [
    Task(name, func)
    for name, func in mod.__dict__.items()
    if name.startswith('Task') and (callable(func) or type(func) == dict)
  ]

  return tasks

def TaskClean(tasks):
  return Task('clean', {
    'description': 'Removes all outs created by other tasks that have the "clean" attribute set as True',
    'actions': [lambda: cleanTasks(tasks)],
  })

def TaskHelp(tasks):
  return Task('help', {
    'description': 'Prints this message',
    'actions': [lambda: printHelp(tasks)],
  })
