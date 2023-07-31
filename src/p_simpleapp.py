"""
https://discourse.panda3d.org/t/make-panda-window-the-active-window/13937/5
https://docs.panda3d.org/1.10/python/programming/configuration/accessing-config-vars-in-a-program



"""
from pathlib import Path

from panda3d.core import loadPrcFile
from panda3d.core import loadPrcFileData
from panda3d.core import ConfigVariableManager

from panda3d.core import ConfigPageManager
from panda3d.core import ConfigVariableString

"""SRC_DIR = Path(__file__).resolve().parent
print("SRC_DIR: ",SRC_DIR)
config = SRC_DIR.as_posix()
file_config = "/config/Config.prc"
path_config = (config +  file_config)
print("config: ",config)
print("path_config: ",path_config)
path_config = f"{path_config}"


loadPrcFile(path_config)"""
loadPrcFile("config/Config.prc")
#loadPrcFileData('', 'fullscreen true')

#cvMgr = ConfigVariableManager.getGlobalPtr()
#cvMgr.listVariables()

from direct.showbase.ShowBase import ShowBase
#from panda3d.core import WindowProperties

class Game(ShowBase):
  def __init__(self):
    ShowBase.__init__(self)

    #wp = WindowProperties()
    #wp.setZOrder(WindowProperties().ZTop)
    #wp.setForeground(True)
    #wp.setTitle('py example')
    #self.win.requestProperties(wp)

    #properties = WindowProperties()
    #properties.setSize(1000, 750)
    #properties.setForeground(True)
    #self.win.requestProperties(properties)

    # get the window properties
    #windowProperties = self.win.getProperties()
    # set the window properties to 'stick on top'
    #windowProperties.setZOrder(windowProperties.ZTop)
    #self.win.requestProperties(windowProperties)
    #self.graphicsEngine.openWindows()
    # set the window properties to 'normal'
    #windowProperties.setZOrder(windowProperties.ZNormal)
    #windowProperties.clearZOrder()
    #self.win.requestProperties(windowProperties)

#if __name__ == "__main__":
  #game = Game()
  #game.run()  

game = Game()
game.run()