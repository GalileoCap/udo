from taskGraph import TaskGraph
from utils import parseArgs, loadTasks

if __name__ == '__main__':
  args = parseArgs()

  tasks = loadTasks(args.file)

  graph = TaskGraph(tasks)
  graph.calcEdges()
  graph.check()
  graph.execute() #TODO: use args.targets
