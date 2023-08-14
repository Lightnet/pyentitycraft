"""
https://discourse.panda3d.org/t/make-panda-window-the-active-window/13937/5
https://arsthaumaturgis.github.io/Panda3DTutorial.io/tutorial/tut_lesson15.html

"""

from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties

# In your "import" statements:
from direct.gui.DirectGui import *

class Game(ShowBase):
  def __init__(self):
    ShowBase.__init__(self)

    wp = WindowProperties()
    wp.setZOrder(WindowProperties().ZTop)
    wp.setForeground(True)
    wp.setTitle('py example')
    self.win.requestProperties(wp)

    self.gameOverScreen = DirectDialog(frameSize = (-0.7, 0.7, -0.7, 0.7),
                                fadeScreen = 0.4,
                                relief = DGG.FLAT)
    label = DirectLabel(text = "Game Over!",
                    parent = self.gameOverScreen,
                    scale = 0.1,
                    pos = (0, 0, 0.2))
    self.finalScoreLabel = DirectLabel(text = "",
                                   parent = self.gameOverScreen,
                                   scale = 0.07,
                                   pos = (0, 0, 0))
    btn = DirectButton(text = "Restart",
                   #command = self.startGame,
                   pos = (-0.3, 0, -0.2),
                   parent = self.gameOverScreen,
                   scale = 0.07)
    btn = DirectButton(text = "Quit",
                   #command = self.quit,
                   pos = (0.3, 0, -0.2),
                   parent = self.gameOverScreen,
                   scale = 0.07)


if __name__ == "__main__":
  game = Game()
  game.run()  