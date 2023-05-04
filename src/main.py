from taskGraph import TaskGraph
from task import loadTasks
from cache import loadCache, saveCache
from init import doInit
from utils import parseArgs, loadModule

if __name__ == '__main__':
  args = parseArgs()

  if args.init:
    doInit(args.file)

  loadCache(args.cache)

  mod = loadModule(args.file)
  tasks = loadTasks(mod)

  graph = TaskGraph(tasks)
  graph.calcEdges()
  graph.check()
  graph.execute(args.targets, force = args.force)

  saveCache(args.cache)
