import maya.cmds as cmds
def toggleCtrls():
	curPanel = cmds.getPanel(withFocus=1)
	if cmds.modelEditor(curPanel,nurbsCurves=1,q=1)==True and cmds.modelEditor(curPanel,nurbsSurfaces=1,q=1)==True:
		cmds.modelEditor(curPanel,e=1,nurbsCurves=0)
		cmds.modelEditor(curPanel,e=1,nurbsSurfaces=0)
	elif cmds.modelEditor(curPanel,nurbsCurves=1,q=1)==False and cmds.modelEditor(curPanel,nurbsSurfaces=1,q=1)==False:
		cmds.modelEditor(curPanel,e=1,nurbsCurves=1)
		cmds.modelEditor(curPanel,e=1,nurbsSurfaces=1)
toggleCtrls()
