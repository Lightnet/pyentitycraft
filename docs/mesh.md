
https://www.youtube.com/watch?v=Z3C9jkYR_7s Panda3D tutorial #27 - procedural mesh generation


https://docs.panda3d.org/1.10/python/programming/internal-structures/other-manipulation/index


https://docs.panda3d.org/1.10/python/programming/internal-structures/procedural-generation/creating-vertex-data

https://docs.panda3d.org/1.10/python/programming/internal-structures/procedural-generation/creating-primitives


```py
#looking at ref...
vdata = GeomVertexData('name', format, Geom.UHStatic)


vdata.setNumRows(4)

vertex = GeomVertexWriter(vdata, 'vertex')
normal = GeomVertexWriter(vdata, 'normal')
color = GeomVertexWriter(vdata, 'color')
texcoord = GeomVertexWriter(vdata, 'texcoord')

vertex.addData3(1, 0, 0)
normal.addData3(0, 0, 1)
color.addData4(0, 0, 1, 1)
texcoord.addData2(1, 0)

vertex.addData3(1, 1, 0)
normal.addData3(0, 0, 1)
color.addData4(0, 0, 1, 1)
texcoord.addData2(1, 1)

vertex.addData3(0, 1, 0)
normal.addData3(0, 0, 1)
color.addData4(0, 0, 1, 1)
texcoord.addData2(0, 1)

vertex.addData3(0, 0, 0)
normal.addData3(0, 0, 1)
color.addData4(0, 0, 1, 1)
texcoord.addData2(0, 0)


prim = GeomTriangles(Geom.UHStatic)

prim.addVertex(0)
prim.addVertex(1)
prim.addVertex(2)
# thats the first triangle

geom = Geom(vdata)
geom.addPrimitive(prim)

node = GeomNode('gnode')
node.addGeom(geom)

nodePath = render.attachNewNode(node)
```