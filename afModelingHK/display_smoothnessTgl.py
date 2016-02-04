# To toggle display smoothness
# hotkey: `
import pymel.core as pm

def tglSmoothDisp():
	cur_smoothness = pm.displaySmoothness(q=1,polygonObject=1)
	if cur_smoothness[0]>1:
		pm.mel.eval("setDisplaySmoothness 1;")
	else:
		pm.mel.eval("setDisplaySmoothness 3;")
tglSmoothDisp()
