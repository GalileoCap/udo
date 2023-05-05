import os

UDOConfig = {
  'version': (1, 3, 0),
}

def TaskBuild():
  return {
    'name': 'build',
    'description': 'Compiles the executable',
    'deps': ['src/main.py', 'src/cache.py', 'src/task.py', 'src/taskGraph.py', 'src/init.py', 'src/utils.py'],
    'outs': ['./build', './build/dist/udo'],

    'actions': [
      'pyinstaller -F src/main.py --name udo --distpath build/dist --workpath build/tmp --specpath build',
    ],
  }

def Tasknstall():
  opath = os.path.expanduser('~/bin/udo')

  return {
    'name': 'install',
    'description': 'Install the executable',
    'deps': ['./build/dist/udo'],
    'outs': [opath],
    'clean': False,

    'actions': [
      f'cp ./build/dist/udo {opath}', 
    ],
  }

#TODO: TaskTest
#TODO: TaskPublish
