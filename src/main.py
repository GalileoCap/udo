import sys

from taskGraph import TaskGraph
from task import loadTasks
from cache import loadCache, saveCache
from init import doInit
from config import loadConfig, checkVersion
from utils import parseArgs, loadModule

if __name__ == '__main__':
  args = parseArgs()

  if args.init:
    doInit(args.file)

  mod = loadModule(args.file)

  loadConfig(mod, args)
  major, minor, patch = checkVersion()
  if not major:
    print('ERROR: Different major version')
    sys.exit(1)

  loadCache()

  tasks = loadTasks(mod)

  graph = TaskGraph(tasks)
  graph.calcEdges()
  graph.check()
  graph.execute(args.targets, force = args.force)

  saveCache()
