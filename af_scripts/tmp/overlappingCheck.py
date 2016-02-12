import itertools
import maya.cmds as cmds

class overlappingCheck(object):
    def __init__(self):
        pass
    
    def _UI(self):
        if cmds.window("checkOverlapWin",q=True,exists=True):
            cmds.deleteUI("checkOverlapWin",window=True)
        w = 200
        w2 = 80
        cmds.window("checkOverlapWin",t="Mesh Overlap Check",s=0,mb=1,rtf=1,w=w)
        cmds.columnLayout("mainColumn",p="checkOverlapWin",columnAttach=('both', 2), rowSpacing=10, columnWidth=w)
        cmds.rowLayout("mainRow",p="mainColumn",w=w,numberOfColumns=2,columnWidth2=(w2,w2),adjustableColumn=2, columnAlign2=[('center'),('center')], columnAttach=[(1, 'both', 1), (2, 'both', 0)])
        cmds.text(p="mainRow",l="Threshold")
        cmds.floatField("thresholdField",p="mainRow",min=0,pre=3,value=0.01)
        cmds.button(p="mainColumn",l="check overlapping",c=self.check_mesh_overlap)
        cmds.showWindow("checkOverlapWin")

	def check_mesh_overlap(self,*args):
		threshold = cmds.floatField("thresholdField",q=True,value=True)
		
		get_sel = cmds.ls(sl=1,fl=1)
		if get_sel and len(get_sel)>1:
			obj_center = [cmds.objectCenter(obj) for obj in get_sel]
			
			#if radio_create_loc:
			locs = []
			for a, b in itertools.combinations(obj_center, 2):
			    distance = ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2) ** 0.5
			    if 0.0 <= distance <= threshold:
					overlapping_loc = cmds.spaceLocator(n="overlapping_loc_1",p=a)
					locs.append(overlapping_loc[0])
					cmds.xform(overlapping_loc,ws=1,piv=a)
			cmds.parent(locs,cmds.group(n=("overlapping_loc_grp"),em=1))
			#elif radio_select_overlap:
			overlap_meshes = []
			for a, b in itertools.combinations(obj_center, 2):
			    distance = ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2) ** 0.5
			    if 0.0 <= distance <= threshold:
			    	for obj in get_sel:
			    		if a == cmds.objectCenter(obj) or b == cmds.objectCenter(obj):
			    			overlap_meshes.append(obj)
			cmds.select(overlap_meshes,r=1)

overlappingCheck()._UI()
