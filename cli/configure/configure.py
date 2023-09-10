from .parser import parse 

class Configure:
  def __init__(self, config):
    self.config = parse(config)

  def begin(self):
    pass

  def finish(self):
    pass
