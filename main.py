import task
import utils

if __name__ == '__main__':
  args = utils.parseArgs()
  print(args)

  mod = utils.importFile(args.file)
  tasks = task.getTasks(mod)
  print(*tasks, sep = '\n')
