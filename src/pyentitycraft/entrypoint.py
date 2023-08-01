
# https://discourse.panda3d.org/t/exception-no-graphics-pipe-is-available-in-python-compiled/26682/12
# https://discourse.panda3d.org/t/need-help-with-exe-making/28136
# https://www.youtube.com/watch?v=xV3gH1JZew4&t=1091s
"""
middle mouse = drag obrit
right mouse=zoom
left mouse=pan
"""

# entry point
from direct.showbase.ShowBase import ShowBase
#from direct.showbase.Loader import Loader
from panda3d.core import loadPrcFile
from panda3d.core import DirectionalLight, AmbientLight

loadPrcFile("config/Config.prc")

class Game(ShowBase):
  def __init__(self):
    ShowBase.__init__(self)

    myblock = loader.loadModel("../assets/block01.glb")
    myblock.reparentTo(render)

    mainlight = DirectionalLight('main light')
    mainLightNodePath = render.attachNewNode(mainlight)
    mainLightNodePath.setHpr(30, -60, 0)
    render.setLight(mainLightNodePath)

    ambientlight=AmbientLight('ambient light')
    ambientlight.setColor((0.3,0.3,0.3,1))
    ambientlightNodePath = render.attachNewNode(ambientlight)
    render.setLight(ambientlightNodePath)

    print("init game...")


def foo():
  print("bar")

#def run():
  #print("Hello World py 2")

#if __name__ == "__main__":
  #game = Game()
  #game.run()  