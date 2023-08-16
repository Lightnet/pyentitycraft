# https://discourse.panda3d.org/t/draw-a-box-sphere-tube-teapot/4506/4
# https://discourse.panda3d.org/t/moving-setting-camera-pos-at-start-solved/2941/2
# https://docs.panda3d.org/1.10/python/programming/tasks-and-events/tasks
# https://docs.panda3d.org/1.10/python/programming/tasks-and-events/index
# https://docs.panda3d.org/1.10/python/programming/intervals/lerp-intervals

import sys
import math
from panda3d.core import Vec3
import direct.directbase.DirectStart
from panda3d.core import GeomVertexFormat, GeomVertexData, GeomVertexWriter, GeomTriangles, Geom, GeomNode, NodePath, GeomPoints

base.setBackgroundColor(0.0, 0.0, 0.0)
base.disableMouse()
camera.setPos(0.0, 0.0, 20.0)
camera.setHpr(0.0, -90.0, 0.0)
#right hold mouse to move up to see cube, it center 0,0,0

class CubeMaker:
    def __init__(self):
        # self.smooth = True/False
        # self.uv = True/False or Spherical/Box/...
        # self.color = Method1/Method2/...
        # self.subdivide = 0/1/2/...
        self.size = 1.0

    def generate(self):
        format = GeomVertexFormat.getV3()
        data = GeomVertexData("Data", format, Geom.UHStatic)
        vertices = GeomVertexWriter(data, "vertex")

        size = self.size
        vertices.addData3f(-size, -size, -size)
        vertices.addData3f(+size, -size, -size)
        vertices.addData3f(-size, +size, -size)
        vertices.addData3f(+size, +size, -size)
        vertices.addData3f(-size, -size, +size)
        vertices.addData3f(+size, -size, +size)
        vertices.addData3f(-size, +size, +size)
        vertices.addData3f(+size, +size, +size)

        triangles = GeomTriangles(Geom.UHStatic)

        def addQuad(v0, v1, v2, v3):
            triangles.addVertices(v0, v1, v2)
            triangles.addVertices(v0, v2, v3)
            triangles.closePrimitive()

        addQuad(4, 5, 7, 6) # Z+
        addQuad(0, 2, 3, 1) # Z-
        addQuad(3, 7, 5, 1) # X+
        addQuad(4, 6, 2, 0) # X-
        addQuad(2, 6, 7, 3) # Y+
        addQuad(0, 1, 5, 4) # Y+

        geom = Geom(data)
        geom.addPrimitive(triangles)

        node = GeomNode("CubeMaker")
        node.addGeom(geom)

        return NodePath(node)

cube = CubeMaker().generate()
cube.setColor(1.0, 0.0, 1.0)
cube.reparentTo(render)
# https://docs.panda3d.org/1.10/python/programming/intervals/lerp-intervals
                                   #time,rotate()
rotation_interval = cube.hprInterval(10,Vec3(45,90,90))
rotation_interval.loop()#loop rotate

#camera.setPos(0.0, 0.0, 20.0)
#base.camera.setPos(0.0,-10.0, 0.0)
#base.camera.setHpr(0.0, -90.0, 0.0)
#camera.reparentTo(render)

base.accept("escape", sys.exit)
base.accept("a", render.analyze)
base.accept("o", base.oobe)

def getCameraPos():
  print(camera)
  print("X: ",camera.getX())
  print("Y: ",camera.getY())
  print("Z: ",camera.getZ())
  camera.setPos(0.0, 0.0, 20.0)
  camera.setHpr(0.0, -90.0, 0.0)
base.accept("w", getCameraPos)

def doSomething(task):
  #cube.setColor(1.0, 0.0, 1.0)
  #print("Hello")
  return task.cont

def taskStop(task):
   taskMgr.remove('Accumulator')

taskMgr.add(doSomething,'doSomething')


base.run()