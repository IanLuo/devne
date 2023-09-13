from .parser import parse 

class Configure:
  def __init__(self, config):
    try:
      self.language = config["language"] + config["version"]
      self.server = config["server"]
    except KeyError as error:
      if error.args[0] == "server":
        self.server = None

  def begin(self):
    pass

  def finish(self):
    pass
