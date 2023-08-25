
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

#from flask_server import testpackage
#testpackage()

import platform
from math import pi, sin, cos
# entry point
from direct.showbase.ShowBase import ShowBase
#from direct.showbase.Loader import Loader
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import loadPrcFile
from panda3d.core import DirectionalLight, AmbientLight
from panda3d.core import TransparencyAttrib
from panda3d.core import WindowProperties
from panda3d.core import CollisionTraverser, CollisionNode, CollisionBox, CollisionRay, CollisionHandlerQueue

#from panda3d.core import 

from direct.gui.DirectGui import DirectButton
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import DirectFrame
from direct.gui.DirectGui import DirectEntry

loadPrcFile("config/Config.prc")

def degToRad(degrees):
  return degrees * (pi / 180.0)

class GameObject():
  pass

class Player(GameObject):
  pass

class Enemy(GameObject):
  pass

class Game(ShowBase):
  # set up
  def __init__(self):
    ShowBase.__init__(self)
    
    print("init game...")

    # Check to make sure keyboard events working
    #self.messenger.toggle_verbose()

    self.selectBlockType = 'grass'
    self.cameraSwingActivated = False
    self.is_menu = False

    self.setupLights()
    self.loadModels()
    self.generateTerrain()
    self.setupSkybox()
    self.setupCamera()
    self.captureMouse()
    self.setupControls()

    self.releaseMouse()#need to do for testing and disable camera move

    self.task_mgr.add(self.update, 'update')

    self.init_menu_network()


    #self.getDataTest()
  def init_menu_network(self):
    print("init network menu")

    self.frame_network = DirectFrame(
      #frameColor=(0, 0, 0, 1),
      frameSize=(-0.5, 0.5, -0.5, 0.5),
      pos=(0, 0, 0)
    )

    textNetwork = OnscreenText(
      parent=self.frame_network,
      text='Network', 
      pos=(0.0, 0.45),
      scale=0.07
    )

    self.entry_server = DirectEntry(
      parent=self.frame_network,
      text = "", 
      scale=.05, 
      #command=setText,
      initialText="localhost", 
      numLines = 2, 
      focus=1, 
      #focusInCommand=clearText
    )
    self.entry_server.setPos(-0.1,0,0.2)

    self.entry_port = DirectEntry(
      parent=self.frame_network,
      text = "", 
      scale=.05, 
      #command=setText,
      initialText="1024", 
      numLines = 2, 
      focus=1, 
      #focusInCommand=clearText
    )
    self.entry_port.setPos(-0.1,0,0.1)

    btn_host = DirectButton(
      parent=self.frame_network,
      text=("HOST"),
      scale=0.07, 
      command=self.init_server
    )
    btn_host.setPos(0.0,0,-0.1)

    btn_join = DirectButton(
      parent=self.frame_network,
      text=("JOIN"),
      scale=0.07, 
      command=self.init_client_join
    )
    btn_join.setPos(0.0,0,-0.2)

  # https://discourse.panda3d.org/t/clever-node-tree-modify-and-restore-how-to/5113/2
  def getDataTest(self):
    #self.dataRootNode()
    #self.render()
    originalScene = self.render.node().copySubgraph()
    print("originalScene:", originalScene)
    for child in originalScene.children:
      #print("node: ", child)
      print("node: ", child.getName())#pass node name
    #self.render.ls()
    return

  def update(self, task):
    dt = globalClock.getDt() #from task loop?

    if self.cameraSwingActivated:
      props = base.win.getProperties()
      actualMode = props.getMouseMode()
      #print("actualMode:", actualMode)

      playerMoveSpeed = 10

      x_movement = 0
      y_movement = 0
      z_movement = 0

      if self.keyMap['forward']:
          x_movement -= dt * playerMoveSpeed * sin(degToRad(camera.getH()))
          y_movement += dt * playerMoveSpeed * cos(degToRad(camera.getH()))
      if self.keyMap['backward']:
          x_movement += dt * playerMoveSpeed * sin(degToRad(camera.getH()))
          y_movement -= dt * playerMoveSpeed * cos(degToRad(camera.getH()))
      if self.keyMap['left']:
          x_movement -= dt * playerMoveSpeed * cos(degToRad(camera.getH()))
          y_movement -= dt * playerMoveSpeed * sin(degToRad(camera.getH()))
      if self.keyMap['right']:
          x_movement += dt * playerMoveSpeed * cos(degToRad(camera.getH()))
          y_movement += dt * playerMoveSpeed * sin(degToRad(camera.getH()))
      if self.keyMap['up']:
          z_movement += dt * playerMoveSpeed
      if self.keyMap['down']:
          z_movement -= dt * playerMoveSpeed

      self.camera.setPos(
        camera.getX() + x_movement,
        camera.getY() + y_movement,
        camera.getZ() + z_movement,
      )

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
        #for os windows that mouse need to be center to able to rotate camera 
        mw = base.mouseWatcherNode
        if mw.hasMouse():
          # get the position, which at center is (0, 0)
          x, y = mw.getMouseX(), mw.getMouseY()
          #add more camera move to rotate camera
          self.cameraSwingFactor = 10000

          mouseChangeX = x
          mouseChangeY = y * -1 #invert camera?

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
    #self.accept('mouse1', self.captureMouse)
    self.accept('mouse1', self.handleLeftClick)
    self.accept('mouse3', self.placeBlock)

    self.accept('w', self.updateKeyMap, ['forward', True])
    self.accept('w-up', self.updateKeyMap, ['forward', False])
    self.accept('s', self.updateKeyMap, ['backward', True])
    self.accept('s-up', self.updateKeyMap, ['backward', False])
    self.accept('a', self.updateKeyMap, ['left', True])
    self.accept('a-up', self.updateKeyMap, ['left', False])
    self.accept('d', self.updateKeyMap, ['right', True])
    self.accept('d-up', self.updateKeyMap, ['right', False])
    self.accept('space', self.updateKeyMap, ['up', True])
    self.accept('space-up', self.updateKeyMap, ['up', False])
    self.accept('lshift', self.updateKeyMap, ['down', True])
    self.accept('lshift-up', self.updateKeyMap, ['down', False]) 

    self.accept('1', self.setSelectBlockType, ['grass']) 
    self.accept('2', self.setSelectBlockType, ['dirt']) 
    self.accept('3', self.setSelectBlockType, ['sand']) 
    self.accept('4', self.setSelectBlockType, ['stone']) 

    self.accept('tab', self.getDataTest) 
  
  def setSelectBlockType(self, type):
    self.selectBlockType = type

  def handleLeftClick(self):
    if self.is_menu:
      self.captureMouse()
      self.removeBlock()

  def removeBlock(self):
    if self.rayQueue.getNumEntries() > 0:
      self.rayQueue.sortEntries()
      rayHit = self.rayQueue.getEntry(0)

      hitNodePath = rayHit.getIntoNodePath()
      hitObject = hitNodePath.getPythonTag('owner')
      distanceFromPlayer = hitObject.getDistance(self.camera)

      if distanceFromPlayer < 12:
        hitNodePath.clearPythonTag('owner')
        hitObject.removeNode()
    
  def placeBlock(self):
    if self.rayQueue.getNumEntries() > 0:
      self.rayQueue.sortEntries()
      rayHit = self.rayQueue.getEntry(0)
      hitNodePath = rayHit.getIntoNodePath()
      normal = rayHit.getSurfaceNormal(hitNodePath)
      hitObject = hitNodePath.getPythonTag('owner')
      distanceFromPlayer = hitObject.getDistance(self.camera)

      if distanceFromPlayer < 12:
        hitBlockPos = hitObject.getPos()
        newBlockPos = hitBlockPos + normal * 2 #block size
        self.createNewBlock(newBlockPos.x,newBlockPos.y,newBlockPos.z, self.selectBlockType)
        

  def updateKeyMap(self, key, value):
    self.keyMap[key] = value

  def captureMouse(self):
    self.cameraSwingActivated = True

    if platform.system() == 'windows':
      #try to center but rotate camera
      mw = base.mouseWatcherNode
      #if mw.hasMouse():
      # get the position, which at center is (0, 0)
      x, y = mw.getMouseX(), mw.getMouseY()
      # move mouse back to center
      props = base.win.getProperties()
      base.win.movePointer(0,
                          props.getXSize() // 2,
                          props.getYSize() // 2)
        # now, x and y can be considered relative movements
    else:#other os
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
    self.camLens.setFov(80)

    crosshairs = OnscreenImage(
      image = '../assets/crosshairs.png',
      pos = (0, 0, 0),
      scale = 0.05
    )
    crosshairs.setTransparency(TransparencyAttrib.MAlpha)

    #ray cast
    self.cTrav = CollisionTraverser()
    ray = CollisionRay()
    ray.setFromLens(self.camNode,(0, 0))
    rayNode = CollisionNode('line-of-sight')
    rayNode.addSolid(ray)
    rayNodePath = self.camera.attachNewNode(rayNode)
    self.rayQueue = CollisionHandlerQueue()
    self.cTrav.addCollider(rayNodePath, self.rayQueue)

  def setupSkybox(self):
    skybox = self.loader.loadModel("../assets/skybox/skybox.egg")
    skybox.setScale(500)
    skybox.setBin('background', 1)
    skybox.setDepthWrite(0)
    skybox.setLightOff()
    skybox.reparentTo(render)

  def generateTerrain(self):

    #for z in range(10):
    for z in range(3):# UP
      for y in range(20):
        for x in range(20):
          #newBlockNode = self.render.attachNewNode('new-block-placeholder')
          self.createNewBlock(
            x * 2 - 20,
            y * 2 - 20,
            -z * 2,
            'grass' if z == 0 else 'dirt'
          )
          
  def createNewBlock(self,x,y,z,type):
    newBlockNode = self.render.attachNewNode('new-block-placeholder')
    newBlockNode.setPos(x, y, z)

    if type == 'grass':
      self.grassBlock.instanceTo(newBlockNode)
    elif type == 'dirt':
      self.dirtBlock.instanceTo(newBlockNode)
    elif type == 'sand':
      self.sandBlock.instanceTo(newBlockNode)
    elif type == 'stone':
      self.stoneBlock.instanceTo(newBlockNode)

    #collision handing...
    blockSolid = CollisionBox((-1, -1, -1),(1, 1, 1))# size 2?
    blockNode = CollisionNode('block-collision-node') #need id name to handle debug? use x,y,z
    blockNode.addSolid(blockSolid)
    collider = newBlockNode.attachNewNode(blockNode)
    collider.setPythonTag('owner', newBlockNode)

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


  def init_server(self):
    print("init server")
    self.frame_network.destroy()
    pass

  def init_client_join(self):
    print("init client")
    self.frame_network.destroy()
    pass
#def foo():
  #print("bar")

#def run():
  #print("Hello World py 2")

#if __name__ == "__main__":
  #game = Game()
  #game.run()  