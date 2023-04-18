def TaskBuild():
  return {
    'name': 'build',
    'description': 'Compiles the executable',
    'deps': ['src/main.py', 'src/cache.py', 'src/task.py', 'src/taskGraph.py', 'src/utils.py'],
    'outs': ['./build', './build/dist/udo'],

    'actions': [
      'pyinstaller -F src/main.py --name udo --distpath build/dist --workpath build/tmp --specpath build',
    ],
  }

#TODO: TaskTest
#TODO: TaskPublish
