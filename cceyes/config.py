import os
import yaml

CONFIG_PATH = os.path.join(os.path.expanduser('~'), '.config/cceyes/config.yaml')

# Load the config
if os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, 'r') as configfile:
        config = yaml.safe_load(configfile)
else:
    config = {}

if 'key' in config.get('api', {}):
    headers = {'X-Api-Key': config['api']['key']}
else:
    headers = {}


def init():
    # create CONFIG_PATH if not exists
    if not os.path.exists(os.path.dirname(CONFIG_PATH)):
        os.makedirs(os.path.dirname(CONFIG_PATH))

    # if api.host is not set in config file, set it to https://api.cceyes.eu
    default = config.setdefault('api', {})
    default.setdefault('host', 'https://api.cceyes.eu')

    # Write the config back to the file
    with open(CONFIG_PATH, 'w') as configfile:
        yaml.safe_dump(config, configfile, default_flow_style=False)


def set_config(parent, key, value):
    config.setdefault(parent, {})[key] = value

    # Write the config back to the file
    with open(CONFIG_PATH, 'w') as configfile:
        yaml.safe_dump(config, configfile, default_flow_style=False)


def get_config(parent, key):
    # if the config value is not set, throw an error
    if parent not in config or key not in config[parent]:
        raise Exception(f"Config value {parent}.{key} is not set")

    return config[parent][key]
