import maya.cmds as cmds
import maya.mel as mel
def createEyelidsPlane():
	curSel = cmds.ls(sl=1,fl=1)
	eyeCtr = cmds.xform(curSel[2],ws=1,piv=1,q=1)[0:3]
	eyeCnra = cmds.pointPosition(curSel[0],w=1)
	eyeCnrb = cmds.pointPosition(curSel[1],w=1)

	eyeballPlane = cmds.polyCreateFacet(n='tmp_eyeball_plane',ch=0,p=[eyeCtr,eyeCnra,eyeCnrb])
	eyelidsPlane  = cmds.polyPlane(n='tmp_eyelids_plane')

	cmds.select((eyelidsPlane[0]+'.vtx[60]'),(eyelidsPlane[0]+'.vtx[70:71]'),(eyeballPlane[0]+'.vtx[0:2]'),r=1)
	mel.eval('snap3PointsTo3Points(0)')
	cmds.select(eyelidsPlane,r=1)
	cmds.xform(eyelidsPlane,os=1,r=1,ro=(0,0,90))
	cmds.delete(eyeballPlane)
createEyelidsPlane()
