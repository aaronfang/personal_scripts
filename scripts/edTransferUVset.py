import pymel.core as pm
def transferUV(source,geo):
	cmds.polyUVSet(geo, rn=True, newUVSet='atlasUV', uvSet= 'map1')
	cmds.polyUVSet(geo, copy=True, uvSet='atlasUV', newUVSet='map1')
	cmds.polyUVSet(geo, currentUVSet=True, uvSet='atlasUV')
	cmds.transferAttributes(source, geo, pos=0, nml=0, uvs=1, col=0, sourceUvSpace='map1', targetUvSet='atlasUV', spa=0)
	cmds.delete(geo, ch=True)
selST = pm.ls(sl=1,sn=1)
transferUV(str(selST[0]),str(selST[1]))
