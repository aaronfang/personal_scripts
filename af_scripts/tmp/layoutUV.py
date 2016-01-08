# select the mesh's shapes and run below commands
import math
sels = cmds.ls(sl=1)
for i, x in enumerate(sels):
    print x
    cmds.select('{0}.map[:]'.format(x), r=1)
    cmds.polyEditUV(u=i % 8, v=int(math.floor(i / 8)))
