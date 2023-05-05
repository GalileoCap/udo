import pickle
import os

from config import config

Cache = {}

def loadCache():
  global Cache

  fpath = config['cache']
  if os.path.exists(fpath):
    with open(fpath, 'rb') as fin:
      Cache = pickle.load(fin)
  else: Cache = {}

def saveCache():
  with open(config['cache'], 'wb') as fin:
    pickle.dump(Cache, fin, protocol = pickle.HIGHEST_PROTOCOL)

def getCache(name):
  return Cache.get(name, {})

def setCache(name, cache):
  if len(cache) != 0:
    Cache[name] = cache
    saveCache()
