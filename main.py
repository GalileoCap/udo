import task
import utils

def executeTaskGraph(tasks):
  #TODO: Change to pseudo-dfs to make it easier to follow
  queue = [task for task in tasks if len(task.parents) == 0]

  while len(queue) != 0:
    task = queue.pop(0)
    task.exec()

    for child in task.children:
      child.exec_visited += 1
      if child.exec_visited == len(child.parents):
        queue.append(child)

if __name__ == '__main__':
  args = utils.parseArgs()
  print(args)

  mod = utils.importFile(args.file)
  tasks = task.loadTasks(mod)
  task.getTaskGraph(tasks)
  executeTaskGraph(tasks)
