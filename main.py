from taskGraph import TaskGraph, loadTasks
from cache import loadCache, saveCache
from utils import parseArgs

if __name__ == '__main__':
  args = parseArgs()

  loadCache() #TODO: args.cachePath

  tasks = loadTasks(args.file)

  graph = TaskGraph(tasks)
  graph.calcEdges()
  graph.check()
  graph.execute() #TODO: use args.targets

  saveCache() #TODO: args.cachePath
