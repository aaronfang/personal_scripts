# move to object

import pymel.core as pm

def move_to_object():
	get_sel = pm.ls(sl=1,fl=1)
	if len(get_sel) == 2:
		src = get_sel[1]
		target = get_sel[0]
		src_oc_x = pm.objectCenter(src,x=1)
		src_oc_y = pm.objectCenter(src,y=1)
		src_oc_z = pm.objectCenter(src,z=1)
		target_oc_x = pm.objectCenter(target,x=1)
		target_oc_y = pm.objectCenter(target,y=1)
		target_oc_z = pm.objectCenter(target,z=1)
		src_oc = [src_oc_x,src_oc_y,src_oc_z]
		target_oc = [target_oc_x,target_oc_y,target_oc_z]
		vector = (src_oc_x-target_oc_x),(src_oc_y-target_oc_y),(src_oc_z-target_oc_z)
		pm.xform(target,t=vector,r=1)
move_to_object()
