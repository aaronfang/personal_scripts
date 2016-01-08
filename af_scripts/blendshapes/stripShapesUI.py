# This script will create blendshape with latest shapes and dial the parameter to 1
import maya.cmds as cmds
global orgGrp
global newGrp
def replaceShapes():
	for newObj in newGrp:
		for orgObj in orgGrp:
			if newObj.split('|')[2] == orgObj.split('|')[2]:
				bp = cmds.blendShape(newObj,orgObj)
				cmds.setAttr(bp[0]+'.'+newObj.split('|')[3],1)

# Strip all the shapes from current blendshapes
global curGeo
global curBS
def stripBS():
	if len(curGeo)!=0 and len(curBS)!=0:
		newShapeGrp = cmds.group(n=(curGeo+'_faceshapes'),em=1)
		tgtShapes = cmds.blendShape(curBS,t=1,q=1)
		for tgt in tgtShapes:
			cmds.setAttr(curBS+'.'+tgt,1)
			newTgt = cmds.duplicate(curGeo,n=tgt)
			cmds.parent(newTgt,newShapeGrp)
			cmds.setAttr(curBS+'.'+tgt,0)
			if newTgt[0].split('_geo')[1].isdigit():
				cmds.rename(newTgt[0],(newTgt[0].split('_geo')[0]+'_geo'))
		#del curGeo
		#del curBS

# UI
def stripShapesUI():
	afBSToolWin = ""
	if cmds.window(afBSToolWin, ex=1):
		cmds.deleteUI(afBSToolWin)
	afBSToolWin = cmds.window(t='StripShapes',tb=1,rtf=1,w=194,h=71)
	cmds.columnLayout(cal='center',adj=1)
	#cmds.button(l='Orginal Group',c=('orgGrp = cmds.ls(sl=1,lf=1,l=1,dag=1,fl=1)'))
	#cmds.button(l='new Group',c=('newGrp = cmds.ls(sl=1,lf=1,l=1,dag=1,fl=1)'))
	#cmds.button(l='Replace Shapes',c=('replaceShapes()'))
	cmds.button(l='Get Geometry',c=('curGeo = cmds.ls(sl=1,fl=1)[0]'))
	cmds.button(l='Get BlendShape Node',c=('curBS = cmds.ls(sl=1,fl=1)[0]'))
	cmds.button(l='Generate Target Shapes',c=('stripBS()'))
	cmds.showWindow(afBSToolWin)
stripShapesUI()
