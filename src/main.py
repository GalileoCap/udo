from taskGraph import TaskGraph
from task import loadTasks
from cache import loadCache, saveCache
from utils import parseArgs

if __name__ == '__main__':
  args = parseArgs()

  loadCache(args.cachePath)

  tasks = loadTasks(args.file)

  graph = TaskGraph(tasks)
  graph.calcEdges()
  graph.check()
  graph.execute(args.targets)

  saveCache(args.cachePath)
