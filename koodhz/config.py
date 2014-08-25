import ConfigParser

class Configuration:
    """this class handles the configuration of all the script"""

    def __init__(self, config_name="config.ini"):
        self.config = ConfigParser.ConfigParser()
        self.config.readfp(open(config_name))

    def __getitem__(self, key):
        """return the item of the general section of the config"""
        value =  self.config.get("Main", key)
        if value in ["yes", "true"]:
            return True
        elif value in ["no", "false"]:
            return False
        if key == "whatsapp.username":
            return value
        try:
            value = int(value)
            return value
        except:
            return value
