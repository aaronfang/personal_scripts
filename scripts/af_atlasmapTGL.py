# This script will switch UV Set between "map1" and "atlasmap".
# Useage:
#   Select meshes which have both map1 and atlas map. Run this script
 
import pymel.core as pm
 
spnd = pm.ls(sl=True, fl=True, dag=True, type='shape')
curUVset = pm.polyUVSet(spnd[0],q=True, currentUVSet=True)
 
if curUVset[0] == 'map1':
    for sp in spnd:
        pm.polyUVSet(sp, currentUVSet=True, uvSet="atlasmap");
elif curUVset[0] == 'atlasmap':
    for sp in spnd:
        pm.polyUVSet(sp, currentUVSet=True, uvSet="map1");
