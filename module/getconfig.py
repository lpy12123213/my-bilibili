from configparser import ConfigParser
def get(file):
    conf = ConfigParser()
    conf.read(file)
    return dict(conf)