import yaml

from utils.classify import Classify

config = Classify(yaml.safe_load(open('config.yaml')))
channels = config.channels
users = config.users
