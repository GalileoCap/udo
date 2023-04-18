import utils

if __name__ == '__main__':
  args = utils.parseArgs()
  print(args)

  mod = utils.importFile(args.file)
  for func in (func for name, func in mod.__dict__.items() if name.startswith('Task')):
    task = func()
    if type(task) == dict:
      print(task)
    elif type(task) == list:
      for subtask in task:
        print(subtask)
