import task
import utils

def executeTaskGraph(tasks):
  pass

if __name__ == '__main__':
  args = utils.parseArgs()
  print(args)

  mod = utils.importFile(args.file)
  tasks = task.loadTasks(mod)
  task.getTaskGraph(tasks)
  executeTaskGraph(tasks)
