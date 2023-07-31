
# https://discourse.panda3d.org/t/exception-no-graphics-pipe-is-available-in-python-compiled/26682/12
# https://discourse.panda3d.org/t/need-help-with-exe-making/28136

# entry point
from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFile

loadPrcFile("config/Config.prc")

class Game(ShowBase):
  def __init__(self):
    ShowBase.__init__(self)
    print("init game.")


def foo():
  print("bar")

#def run():
  #print("Hello World py 2")

#if __name__ == "__main__":
  #game = Game()
  #game.run()  