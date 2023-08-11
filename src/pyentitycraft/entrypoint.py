
# https://discourse.panda3d.org/t/exception-no-graphics-pipe-is-available-in-python-compiled/26682/12
# https://discourse.panda3d.org/t/need-help-with-exe-making/28136
# https://www.youtube.com/watch?v=xV3gH1JZew4&t=1091s
# https://docs.panda3d.org/1.10/python/programming/hardware-support/mouse-support mouse input lock??
# https://docs.panda3d.org/1.10/python/reference/panda3d.core.WindowProperties#panda3d.core.WindowProperties
"""
middle mouse = drag obrit
right mouse=zoom
left mouse=pan
"""
import platform
# entry point
from direct.showbase.ShowBase import ShowBase
#from direct.showbase.Loader import Loader
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import loadPrcFile
from panda3d.core import DirectionalLight, AmbientLight
from panda3d.core import TransparencyAttrib
from panda3d.core import WindowProperties



loadPrcFile("config/Config.prc")

class Game(ShowBase):
  def __init__(self):
    ShowBase.__init__(self)
    
    print("init game...")

    self.setupLights()
    self.loadModels()
    self.generateTerrain()
    self.setupSkybox()
    self.setupCamera()
    self.captureMouse()
    self.setupControls()

    self.task_mgr.add(self.update, 'update')

  def update(self, task):
    dt = globalClock.getDt()

    if self.cameraSwingActivated:
      props = base.win.getProperties()
      actualMode = props.getMouseMode()
      #print("actualMode:", actualMode)

      if actualMode == WindowProperties.M_relative:
        md = self.win.getPointer(0)
        mouseX = md.getX()
        mouseY = md.getY()

        mouseChangeX = mouseX - self.LastMouseX
        mouseChangeY = mouseY - self.LastMouseY

        self.cameraSwingFactor = 10

        currentH = self.camera.getH()
        currentP = self.camera.getP()

        self.camera.setHpr(
          currentH - mouseChangeX * dt * self.cameraSwingFactor,
          min(90, max(-90, currentP - mouseChangeY * dt * self.cameraSwingFactor)),
          0
        )
        self.LastMouseX = mouseX
        self.LastMouseY = mouseY
      else:
        mw = base.mouseWatcherNode
        if mw.hasMouse():
          # get the position, which at center is (0, 0)
          x, y = mw.getMouseX(), mw.getMouseY()

          self.cameraSwingFactor = 10000

          mouseChangeX = x
          mouseChangeY = y * -1

          currentH = self.camera.getH()
          currentP = self.camera.getP()

          self.camera.setHpr(
            currentH - mouseChangeX * dt * self.cameraSwingFactor,
            min(90, max(-90, currentP - mouseChangeY * dt * self.cameraSwingFactor)),
            0
          )

          # move mouse back to center
          props = base.win.getProperties()
          base.win.movePointer(0,
                              props.getXSize() // 2,
                              props.getYSize() // 2)
          # now, x and y can be considered relative movements
          # https://docs.panda3d.org/1.10/python/programming/hardware-support/mouse-support
        
    return task.cont

  def setupControls(self):
    self.keyMap = {
      "forward":False,
      "backward":False,
      "left":False,
      "right":False,
      "up":False,
      "down":False,
    }

    self.accept('escape', self.releaseMouse)
    self.accept('mouse1', self.captureMouse)

  def captureMouse(self):
    self.cameraSwingActivated = True

    md = self.win.getPointer(0)
    self.LastMouseX = md.getX()
    self.LastMouseY = md.getY()

    properties = WindowProperties()
    properties.setCursorHidden(True)
    print("platform.system(): ", platform.system())
    if platform.system() == 'windows':
      properties.setMouseMode(WindowProperties.M_confined) # windows
    else:
      properties.setMouseMode(WindowProperties.M_relative) # mac & linux
    
    self.win.requestProperties(properties)
    #self.base.win.requestProperties(properties)
  
  def releaseMouse(self):
    self.cameraSwingActivated = False
    properties = WindowProperties()
    properties.setCursorHidden(False)
    properties.setMouseMode(WindowProperties.M_absolute)
    self.win.requestProperties(properties)
    #self.base.win.requestProperties(properties)

  def setupCamera(self):
    self.disable_mouse()
    self.camera.setPos(0, 0, 3)

    crosshairs = OnscreenImage(
      image = '../assets/crosshairs.png',
      pos = (0, 0, 0),
      scale = 0.05
    )
    crosshairs.setTransparency(TransparencyAttrib.MAlpha)

  def setupSkybox(self):
    skybox = self.loader.loadModel("../assets/skybox/skybox.egg")
    skybox.setScale(500)
    skybox.setBin('background', 1)
    skybox.setDepthWrite(0)
    skybox.setLightOff()
    skybox.reparentTo(render)

  def generateTerrain(self):

    for z in range(10):
      for y in range(20):
        for x in range(20):
          newBlockNode = self.render.attachNewNode('new-block-placeholder')
          newBlockNode.setPos(
            x * 2 - 20,
            y * 2 - 20,
            -z * 2
          )
          if z == 0:
            self.grassBlock.instanceTo(newBlockNode)
          else:
            self.dirtBlock.instanceTo(newBlockNode)

  def setupLights(self):
    mainlight = DirectionalLight('main light')
    mainLightNodePath = self.render.attachNewNode(mainlight)
    mainLightNodePath.setHpr(30, -60, 0)
    self.render.setLight(mainLightNodePath)

    ambientlight=AmbientLight('ambient light')
    ambientlight.setColor((0.3,0.3,0.3,1))
    ambientlightNodePath = self.render.attachNewNode(ambientlight)
    self.render.setLight(ambientlightNodePath)

  def loadModels(self):
    #self.myblock = self.loader.loadModel("../assets/block01.glb")
    #self.myblock.setPos(2,2,0)
    #self.myblock.reparentTo(self.render)
    #self.myblock.reparentTo(render) # alt from class extend? vscode see error?

    #self.entity_player = loader.loadModel("../assets/mc_player01.glb")
    #self.entity_player.reparentTo(render)

    self.grassBlock = self.loader.loadModel("../assets/grass-block.glb")
    #self.grassBlock.reparentTo(self.render)

    self.dirtBlock = self.loader.loadModel("../assets/dirt-block.glb")
    #self.dirtBlock.setPos(0,2,0)
    #self.dirtBlock.reparentTo(self.render)

    self.stoneBlock = self.loader.loadModel("../assets/stone-block.glb")
    #self.stoneBlock.setPos(0,-2,0)
    #self.stoneBlock.reparentTo(self.render)

    self.sandBlock = self.loader.loadModel("../assets/sand-block.glb")
    #self.sandBlock.setPos(0,4,0)
    #self.sandBlock.reparentTo(self.render)

#def foo():
  #print("bar")

#def run():
  #print("Hello World py 2")

#if __name__ == "__main__":
  #game = Game()
  #game.run()  