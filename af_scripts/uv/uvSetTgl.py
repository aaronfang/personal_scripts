# This script will switch UV Set between "map1" and "atlasmap".
# Useage:
# Select meshes and run this script
import maya.cmds as cmds
def uvsetTgl():
    shape_node = cmds.ls(sl=True, fl=True, dag=True, type='shape')
    current_uvset = cmds.polyUVSet(shape_node[0],q=True, currentUVSet=True)
    
    for shape in shape_node:
        uvsets = cmds.polyUVSet(shape,q=True,auv=True)
        if "map1" and "atlasUV" in uvsets:
            if current_uvset[0] == 'map1':
                cmds.polyUVSet(shape, currentUVSet=True, uvSet="atlasUV")
            elif current_uvset[0] == 'atlasUV':
                cmds.polyUVSet(shape, currentUVSet=True, uvSet="map1")
            else:
                cmds.polyUVSet(shape, currentUVSet=True, uvSet="map1")
        elif "map1" in uvsets and "atlasUV" not in uvsets:
            cmds.polyUVSet(shape, currentUVSet=True, uvSet="map1")
uvsetTgl()
