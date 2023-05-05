from utils import currVersion, dfltCache, dfltPrefix

config = {
  'version': currVersion,
  'cache': dfltCache,
  'prefix': dfltPrefix,
}

def loadConfig(mod, args):
  global config
  _config = mod.__dict__.get('UDOConfig', config)
  for key, value in _config.items():
    config[key] = value

  # Prioritize arguments
  if args.cache is not None:
    config['cache'] = args.cache
  if args.prefix is not None:
    config['prefix'] = args.prefix

def checkVersion():
  # TODO: Check config['version'] is correct type and lenght
  return [currVersion[idx] == config['version'][idx] for idx in range(len(currVersion))]
