import itertools
import maya.cmds as cmds
import math

class overlappingCheck(object):
	def __init__(self):
		pass

	def _UI(self):
		if cmds.window("checkOverlapWin",q=True,exists=True):
			cmds.deleteUI("checkOverlapWin",window=True)
		w = 200
		w2 = 70
		cmds.window("checkOverlapWin",t="Mesh Overlap Check",s=0,mb=1,rtf=1,w=w,mnb=0,mxb=0)
		cmds.columnLayout("mainColumn",p="checkOverlapWin",columnAttach=('both', 2), rowSpacing=10, columnWidth=w)
		cmds.rowLayout("mainRow",p="mainColumn",w=w,numberOfColumns=3,columnWidth3=(w2,50,w2),adjustableColumn=2, columnAlign3=[('center'),('center'),('center')], columnAttach=[(1, 'both', 1), (2, 'both', 0), (3, 'both', 0)])
		cmds.text(p="mainRow",l="Threshold")
		cmds.floatField("thresholdField",p="mainRow",min=0,pre=3,value=0.01)
		cmds.button(p="mainRow",l="get distance",c=self.get_distance)
		
		cmds.checkBox("centerCheck",p="mainColumn",l="similar position",ed=0,al="center",v=1)
		cmds.checkBox("bboxCheck",p="mainColumn",l="similar sizes", al="center",v=0)
		cmds.button(p="mainColumn",l="check overlapping",c=self.check_object_overlap)

		cmds.separator(p="mainColumn",style='in')
		cmds.textScrollList("overlapListTextScroll",p="mainColumn",numberOfRows=8,allowMultiSelection=True,sc=self.select_item)

		cmds.showWindow("checkOverlapWin")

	def check_object_overlap(self,*args):
		cmds.textScrollList("overlapListTextScroll",e=True,ra=True)
		self.threshold = cmds.floatField("thresholdField",q=True,value=True)
		get_sel = cmds.ls(sl=1,fl=1,type="transform",o=1)
		if get_sel and len(get_sel)>1:
			obj_center = []
			for obj in get_sel:
				oc = cmds.objectCenter(obj)
				occ = [obj,oc]
				obj_center.append(occ)
			overlap_center = []
			overlap_bbox = []
			for a, b in itertools.combinations(obj_center, 2):
				distance = ((a[1][0] - b[1][0]) ** 2 + (a[1][1] - b[1][1]) ** 2 + (a[1][2] - b[1][2]) ** 2) ** 0.5
				if 0<=distance<=self.threshold:
					ab = (a[0],b[0])
					overlap_center.append(ab)
					for meshes in overlap_center:
						bboxA = cmds.polyEvaluate(meshes[0],b=True)
						bboxB = cmds.polyEvaluate(meshes[1],b=True)
						diameter_bboxA = ((bboxA[0][1] - bboxA[0][0]) ** 2 + (bboxA[1][1] - bboxA[1][0]) ** 2 + (bboxA[2][1] - bboxA[2][1]) ** 2) ** 0.5
						diameter_bboxB = ((bboxB[0][1] - bboxB[0][0]) ** 2 + (bboxB[1][1] - bboxB[1][0]) ** 2 + (bboxB[2][1] - bboxB[2][1]) ** 2) ** 0.5
						diff = abs(diameter_bboxA - diameter_bboxB)
						if 0<= diff <= self.threshold:
							if meshes not in overlap_bbox:
								overlap_bbox.append(meshes)
	
			if cmds.checkBox("bboxCheck",q=True,v=True) == 0:
				item_list = []
				for item in overlap_center:
					for x in item:
						item_list.append(x)
				item_list = list(set(item_list))
				cmds.textScrollList("overlapListTextScroll",e=True,a=item_list)
				cmds.select(cmds.textScrollList("overlapListTextScroll",q=True,ai=True),r=1)
				
			elif cmds.checkBox("bboxCheck",q=True,v=True) == 1:
				item_list = []
				for item in overlap_bbox:
					for x in item:
						item_list.append(x)
				item_list = list(set(item_list))
				cmds.textScrollList("overlapListTextScroll",e=True,a=item_list)
				cmds.select(cmds.textScrollList("overlapListTextScroll",q=True,ai=True),r=1)

	def select_item(self,*args):
		sel_in_list = cmds.textScrollList("overlapListTextScroll",q=True,si=True)
		if sel_in_list != None:
			for item in sel_in_list:
				if item not in cmds.ls(type="transform",o=1,fl=1):
					cmds.textScrollList("overlapListTextScroll",e=True,ri=item)
		cmds.select(sel_in_list,r=1)

	def get_distance(self,*args):
		get_sel = cmds.ls(sl=1,fl=1,type="transform",o=1)
		if get_sel and len(get_sel)==2:
			obj_center = [cmds.objectCenter(obj) for obj in get_sel]
			a,b = obj_center
			distance = ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2) ** 0.5
			cmds.floatField("thresholdField",e=True,v=distance)
			dist_in_field = cmds.floatField("thresholdField",q=True,value=True)
			if distance > dist_in_field:
				dist = dist_in_field + 0.001
				cmds.floatField("thresholdField",e=True,v=dist)
		else:
			cmds.confirmDialog(m="Please select 2 meshes close to each other to calculate the distance!",b="ok")
overlappingCheck()._UI()
