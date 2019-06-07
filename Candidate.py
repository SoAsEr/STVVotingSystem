class Candidate:
  def __init__(self, name, root=False):
    self.name = name
    self.weight=1
    self.lost=root
    self.won=False
    self.votes=0
