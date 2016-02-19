# blendshape tools
# - import and replace current target shapes
# - export target shapes as separate objs
# - expand shapes in viewport 
# - create blendshape based on selection(src/target) and lock the src
# - display blendshape target sliders for selected src geometries
# - add/remove blendshape targets
# - add/remove in-between shapes based on naming
# - update in-between positions by updating naming
# - modify in-between shape in solo mode
# - toggle in-between shape with before/after
# - export high-res weight map
# - update target shapes by blendshape weights
# - check model symmetry
# - mirror half(continusily model)
# - mirror half(separated model)
# - freeze transform for all vertices
# - update all target shapes and in-between shapes based on naming
# - corrective shape create/connect/modify
# - paint weight enhance functions:
#     - reverse value
#     - add/reduce value for non-zero areas
#     - mark all border as 0
#     - weightmap list for save/load
#     - increase/decrease area
#     - mirror weights
import pymel.core as pm

class blendshapeV2UI(object):
	def __init__(self):
		pass
	def _UI(self):
		if pm.window("BSMainWin",exists=1):
			pm.deleteUI("BSMainWin",window=1)
		w=300
		window=pm.window("BSMainWin",t="BlendShape Tools",s=0,rtf=1,mb=1,w=w)
		pm.columnLayout("mainColumn",p="BSMainWin",columnAttach=('both', 2), rowSpacing=10, columnWidth=w)
		
		pm.showWindow("BSMainWin")
		
	def refreshBSList(self,*args):
		getSel = pm.ls(sl=1,fl=1)
		BSNode = pm.ls(pm.listHistory(getSel[0]) or [],type='blendShape')
		tgtGrp = pm.blendShape(BSNode[0],t=1,q=1)
		for tgt in tgtGrp:
			pm.
		
blendshapeV2UI()._UI()
