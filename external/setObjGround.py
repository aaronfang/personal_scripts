from pymel.core import *

allSel = ls(sl=True)
objs = allSel[0:-1]
terrain = allSel[-1]

for x in objs:
    objPos = getAttr(x + '.translate')
    geoConstraint = geometryConstraint(terrain, x)
    select(x)
    move(objPos.x, objPos.z, a=True, moveXZ=True)
    delete(geoConstraint)
    select(d=True)
