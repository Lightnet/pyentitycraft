"""
https://discourse.panda3d.org/t/make-panda-window-the-active-window/13937/5


"""

from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        wp = WindowProperties()
        wp.setZOrder(WindowProperties().ZTop)
        wp.setForeground(True)
        wp.setTitle('py example')
        self.win.requestProperties(wp)

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

if __name__ == "__main__":
  game = Game()
  game.run()  