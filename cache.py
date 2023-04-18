import pickle
import os

Cache = {}

def loadCache(fpath = '.udo.db'):
  global Cache

  if os.path.exists(fpath):
    with open(fpath, 'rb') as fin:
      Cache = pickle.load(fin)
  else: Cache = {}

def saveCache(fpath = '.udo.db'):
  with open(fpath, 'wb') as fin:
    pickle.dump(Cache, fin, protocol = pickle.HIGHEST_PROTOCOL)

def getCache(name):
  return Cache.get(name, {})

def setCache(name, cache):
  if len(cache) != 0:
    Cache[name] = cache
