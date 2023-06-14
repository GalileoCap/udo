############################################################
# S: Utils #################################################

import os
from pathlib import Path

def filesWithExtension(d, extension):
  return [ str(fpath) for fpath in list(Path(d).rglob(f'*{extension}')) ]

############################################################
# S: Config ################################################

UDOConfig = {
  'version': (1, 4, 0),
}

SRCD = 'src'
BUILDD = 'build'
DOCSD = 'docs'

TMPD = os.path.join(BUILDD, 'tmp')
DISTDD = os.path.join(BUILDD, 'dist')
CONTENTD = os.path.join(DOCSD, 'content')
PUBLICD = os.path.join(DOCSD, 'public')

NAME = 'udo'
SRC = filesWithExtension(SRCD, '.py')
BIN = os.path.join(DISTDD, NAME)
INSTALLBIN = os.path.join(os.path.expanduser('/usr/local/bin'), NAME)

DOCS = filesWithExtension(CONTENTD, '.md')

############################################################
# S: Tasks #################################################

def TaskBuild():
  return {
    'name': 'build',
    'description': 'Compiles the executable',
    'deps': SRC,
    'outs': [BUILDD, BIN],

    'actions': [
      f'pyinstaller -F src/main.py --name {NAME} --distpath {DISTDD} --workpath {TMPD} --specpath {BUILDD}',
    ],
  }

def TaskInstall():
  return {
    'name': 'install',
    'description': 'Install the executable',
    'deps': [BIN],
    'outs': [INSTALLBIN],
    'clean': False, # TODO: input()... but remove with sudo
    # 'clean': lambda: input('Uninstall? [y/N]').lower() in ['y', 'ye', 'yes', 'yes!', 'yea', 'yeah', 'yeah!'],

    'actions': [
      f'sudo cp {BIN} {INSTALLBIN}', 
    ],
  }

def TaskPublish():
  return {
    'name': 'publish',
    'description': 'Publish site',
    'deps': DOCS,
    'skipRun': True, # TODO: Check git branch is main

    'actions': [
      f'hugo -s {DOCSD} --minify',
      f'git add {DOCSD} && git commit -m "Deploy site"', # TODO: Get last commit
      f'git subtree push --prefix {PUBLICD} origin gh-pages', # SEE: https://gist.github.com/cobyism/4730490
    ],
  }

#TODO: TaskTest
