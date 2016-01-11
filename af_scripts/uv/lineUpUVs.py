import pymel.core as pm
import math
def lineUpUVs():
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
lineUpUVs()
