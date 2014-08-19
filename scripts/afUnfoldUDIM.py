import pymel.core as pm
import math
import maya.mel as mm

def afUnfoldUDIM():
    #select UV shells
    mm.eval("PolySelectConvert 1")
    
    UVBbox = pm.polyEvaluate(curSelUVs, bc2 = True)
    UPos = int(math.floor(UVBbox[0][0]))
    VPos = int(math.floor(UVBbox[1][0]))
    #udim = int(VPos*10 + UPos + 1001)
    
    mm.eval("RoadkillProOrganic")
    
    pm.polyEditUV(u=UPos,v=VPos,r=True)
    mm.eval("PolySelectConvert 4")
afUnfoldUDIM()
