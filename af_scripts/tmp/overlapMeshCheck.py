import itertools
import maya.cmds as cmds

threshold = 0.1

get_sel = cmds.ls(sl=1,fl=1)
obj_center = [cmds.objectCenter(obj) for obj in get_sel]

if radio_create_loc:
	locs=[]
	for a, b in itertools.combinations(obj_center, 2):
	    distance = ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2) ** 0.5
	    if 0.0 <= distance <= threshold:
			overlapping_loc = cmds.spaceLocator(n="overlapping_loc_1",p=a)
			locs.append(overlapping_loc[0])
			cmds.xform(overlapping_loc,ws=1,piv=a)
	cmds.select(locs,r=1)
elif radio_select_overlap:
	for a, b in itertools.combinations(obj_center, 2):
	    distance = ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2) ** 0.5
	    if 0.0 <= distance <= threshold:
	    	cmds.select(


