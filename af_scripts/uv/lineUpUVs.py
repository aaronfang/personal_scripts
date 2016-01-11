import pymel.core as pm
import math

class lineUpUVs(object):
	def __init__(self):
		self.window=""
		pass
	
	def _UI(self):
		if pm.window(self.window,exists=1):
			pm.deleteUI(self.window)
		self.window=pm.window(t="template window",s=1,mb=1,rtf=1,wh=(300,500))
		pm.columnLayout()
			self.button=pm.button(l="Template Button",wh=(100,10),bc="templateFunc")
		pm.showWindow(self.window)

	def lineUpU():
		sels = pm.ls(sl=1)
		gap = 0.003
		for i, x in enumerate(sels):
			x=x.getShape()
			pm.select('{0}.map[:]'.format(x), r=1)
			buv = pm.polyEvaluate(x,b2=1)
			w = abs(buv[0][1] - buv[0][0])
			if i==0:
				pm.polyEditUV(u=-buv[0][0]+(gap*(i+1)),v=-buv[1][0]+gap)
			else:
				pm.polyEditUV(u=-buv[0][0]+(w*i+gap*(i+1)),v=-buv[1][0]+gap)
		pm.select(sels,r=1)

	def lineUpV():
		sels = pm.ls(sl=1)
		gap = 0.003
		for i, x in enumerate(sels):
			x=x.getShape()
			pm.select('{0}.map[:]'.format(x), r=1)
			buv = pm.polyEvaluate(x,b2=1)
			w = abs(buv[1][1] - buv[1][0])
			if i==0:
				pm.polyEditUV(v=-buv[1][1]-(gap*(i+1)),u=-buv[0][0]+gap)
			else:
				pm.polyEditUV(v=-buv[1][1]-(w*i+gap*(i+1)),u=-buv[0][0]+gap)
		pm.select(sels,r=1)

lineUpUVs()._UI()