'''
select inside the loop:
	- select an edge/face/vert loop and a vtx/edge/face inside of loop
	- get loop and convert to edges
	- create a temp uvset and give a planer map
	- separate uvs into shells based on edge loop
	- select the uv shell contains the last selection and convert to face
	- remove the temp uvset

use scriptJob for condition change
use hilite for highlight current selection

'''
import maya.cmds as cmds
#import afCore.cmds as ac
get_sel = cmds.ls(sl=True,fl=True)
last_comp = get_sel[-1]
loop_comp = get_sel[:-1]
if ac.is_comp(get_sel) == "face":
	edge_loop = ac.convert_comp(f=loop_comp,el=1)
	cmds.uvSet("temp_uvset_for_selection",create=1)
	cmds.cutUV(edge_loop)
	cmds.select(last_comp,r=True)
	cmds.toShell()
	cmes.toface()
	cmds.delete("temp_uvset_for_selection",uvSet=1)
	