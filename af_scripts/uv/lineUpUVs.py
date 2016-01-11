import pymel.core as pm
import math

class lineUpUVs(object):
	def __init__(self):
		self.window=""
		pass
	
	def _UI(self):
		if pm.window(self.window,exists=1):
			pm.deleteUI(self.window)
		self.window=pm.window(t="LineUp UVs Window",s=1,mb=1,rtf=1,wh=(300,500))
		pm.columnLayout()
			self.textField=pm.textField(l="Gap",text="0.003")
			self.button=pm.button(l="lineUp Horizontaly",wh=(100,10),bc="lineUpU()")
			self.button=pm.button(l="lineUp Verticaly",wh=(100,10),bc="lineUpV()")
		pm.showWindow(self.window)

	def lineUpU():
		sels = pm.ls(sl=1)
		gap = pm.textField(self.textField,q=True,text=True)
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
		gap = pm.textField(self.textField,q=True,text=True)
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