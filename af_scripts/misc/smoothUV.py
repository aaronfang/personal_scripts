import pymel.core as pm
def setSmoothUV():
	curSel = pm.ls(sl=1,fl=1)
	for sel in curSel:
		sel = sel.getShape()
		pm.setAttr(sel + '.osdVertBoundary',2)
		pm.setAttr(sel + '.osdFvarBoundary',1)
		pm.setAttr(sel + '.keepMapBorders',0)
setSmoothUV()
