from utils import currVersion

config = {
  'version': currVersion,
}

def loadConfig(mod):
  global config
  _config = mod.__dict__.get('UDOConfig', config)
  for key, value in _config.items():
    config[key] = value

def checkVersion():
  # TODO: Check config['version'] is correct type and lenght
  return [currVersion[idx] == config['version'][idx] for idx in range(len(currVersion))]
