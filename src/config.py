from utils import currVersion, dfltCache, dfltPrefix, dfltForceAll

config = {
  'version': currVersion,
  'cache': dfltCache,
  'prefix': dfltPrefix,
  'force': [],
  'forceAll': dfltForceAll,
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
  if len(args.force) != 0:
    config['force'] = args.force.split(',')
    print(config['force'], args.force)
  if args.forceAll is not None:
    config['forceAll'] = args.forceAll

def checkVersion():
  # TODO: Check config['version'] is correct type and lenght
  return [currVersion[idx] == config['version'][idx] for idx in range(len(currVersion))]
