import pymel.core as pm
import math

UVs = pm.polyEvaluate('l_ear_part', bc2 = True)
print UVs
ss = math.floor(UVs[0][0])
tt = math.floor(UVs[1][0])
udim = int(tt*10 + ss + 1001)
print udim
