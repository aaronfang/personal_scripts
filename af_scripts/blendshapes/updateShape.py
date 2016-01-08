# update shapes.
# select new shapes and old shapes
import maya.cmds as cmds
import maya.mel as mel
def updateShape():
	bsTgt = cmds.ls(sl=1,fl=1)
	newSp = bsTgt[0]
	orgSp = bsTgt[1]
	bsNd = cmds.blendShape(newSp,orgSp)
	cmds.setAttr(bsNd[0]+'.'+newSp,1)
	cmds.select(orgSp,r=1)
	mel.eval('DeleteHistory')
	cmds.delete(newSp)
updateShape()
