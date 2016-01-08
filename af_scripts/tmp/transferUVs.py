import maya.cmds as cmds
import pymel.core as pm

curSel = pm.ls(sl=1,fl=1)
getSd = curSel[0].MaterialInfo()
for sel in curSel[1:]:
	cmds.transferAttributes(curSel[0],sel,pos=0,nml=0,uvs=2,col=0,spa=5,sus='map1',tus='map1',sm=3,fuv=0,clb=1)
	cmds.sets(sel,e -forceElement af_checker_LambertSG;
