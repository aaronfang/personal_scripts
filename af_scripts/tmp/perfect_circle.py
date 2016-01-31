import pymel.core as pm
import re
pm.selectPref(trackSelectionOrder=True)

getSel  = pm.ls(os=1)
vtxGrp = pm.ls(pm.polyListComponentConversion(getSel,fe=1,tv=1),fl=1)
vtxNum = len(vtxGrp)

vtxPosGrp = [pm.xform(vtx, q=True, ws=True, t=True)for vtx in vtxGrp]

tmpPoly = mc.polyCreateFacet(p=[tuple(vec) for vec in vtxPosGrp ])[0]
pm.xform(tmpPoly,cp=1)
centerPos = mc.xform(tmpPoly, q=True, ws=True, rp=True)
distGrp = [((vec[0] - centerPos[0]) ** 2 + (vec[1] - centerPos[1]) ** 2 + (vec[2] - centerPos[2]) ** 2) ** 0.5 for vec in vtxPosGrp]
dist = sum(distGrp)/vtxNum

circle = pm.circle(s=vtxNum, r=dist, c=(0, 0, 0), d=3, ch=False)[0]
pm.xform(circle, ws=True, t=tuple(centerPos))

wu = (vtxPosGrp[0][0] - centerPos[0]),(vtxPosGrp[0][1] - centerPos[1]),(vtxPosGrp[0][2] - centerPos[2])

pm.normalConstraint(tmpPoly,circle,aim=[0,0,1],u=[0,1,0],wu=(0,1,0))

e2vInfos= pm.polyInfo(getSel,ev=1)
e2vDict = {}
for info in e2vInfos:
    evList = [ int(i) for i in re.findall('\\d+', info) ]
    e2vDict.update(dict([(evList[0], evList[1:])]))


# average normal
vtxGrp = pm.mel.eval("PolySelectConvert 3;")
avNmGrp = pm.polyNormalPerVertex(getSel,q=1,xyz=1)
