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

def TaskInstall():
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

def TaskPublish():
  return {
    'name': 'publish',
    'description': 'Publish site',
    'deps': ['./docs/content/_index.md', './docs/content/api.md', './docs/content/examples/basic.md', './docs/content/menu/index.md', './docs/content/posts/_index.md', './docs/content/quick-start.md'],
    'skipRun': True, # TODO: Check git branch is main

    'actions': [
      'hugo -s docs --minify',
      'git add docs && git commit -m "Deploy site"', # TODO: Get last commit
      'git subtree push --prefix docs/public origin gh-pages',
    ],
  }

#TODO: TaskTest
#TODO: TaskPublish
