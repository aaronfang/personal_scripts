# auto generate atlasUV for all selected meshes
import maya.cmds as cmds


meshes = cmds.ls(sl=1, fl=1)
for mesh in meshes:
    allUVSets = cmds.polyUVSet(mesh,q=1,auv=1)
    if 'atlasUV' in allUVSets:
        cmds.polyUVSet(mesh, delete=True, uvSet='atlasUV')
    cmds.polyUVSet(mesh, copy=True, uvSet='map1', newUVSet='atlasUV')
    cmds.polyUVSet(mesh, currentUVSet=True, uvSet='atlasUV')
cmds.polyMultiLayoutUV(meshes,uvs="atlasUV",l=2,rbf=1,sc=1,lm=1,fr=1,ps=0.2)


# toggle between map1 and atlasUV
# This script will switch UV Set between "map1" and "atlasmap".
# Useage:
# Select meshes which have both map1 and atlas map. Run this script
import maya.cmds as cmds


spnd = cmds.ls(sl=True, fl=True, dag=True, type='shape')
curUVset = cmds.polyUVSet(spnd[0],q=True, currentUVSet=True)
if curUVset[0] == 'map1':
	for sp in spnd:
		cmds.polyUVSet(sp, currentUVSet=True, uvSet="atlasUV")
elif curUVset[0] == 'atlasUV':
	for sp in spnd:
		cmds.polyUVSet(sp, currentUVSet=True, uvSet="map1")
