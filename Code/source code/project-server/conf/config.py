import yaml
class Config:
    def __init__(self, conf_path='./conf.yaml'):
        try:
            with open(conf_path, 'r') as f:
                self.cfg = yaml.safe_load(f)
                print("Init config success...")
        except:
            print("Config file not exists!")

config = Config('conf/conf.yaml')