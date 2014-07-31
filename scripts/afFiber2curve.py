import pymel.core as pm
import maya.mel as mel

curSel = pm.ls(sl=1,fl=1)
for hair in curSel:
  pm.select(hair + '.e[1]',r=1)
  mel.eval("SelectEdgeLoopSp;")
  pm.polyToCurve(form=2,degree=3)
  pm.select(cl=1)
