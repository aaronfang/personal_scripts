import pymel.core as pm
import maya.mel as mel

allSets = pm.ls(sl=1,type="objectSet")

for i in range(0,len(allSets)):
    if i<10:
        pm.select(allSets[i],r=1,ne=1)
        pm.select(hierarchy=1)
        mel.eval("ConvertSelectionToUVs;")
        pm.polyEditUV(u=i,v=0)
    elif i>=10<20:
        pm.select(allSets[i],r=1,ne=1)
        pm.select(hierarchy=1)
        mel.eval("ConvertSelectionToUVs;")
        pm.polyEditUV(u=i-10,v=1)
    elif i>=20<30:
        pm.select(allSets[i],r=1,ne=1)
        pm.select(hierarchy=1)
        mel.eval("ConvertSelectionToUVs;")
        pm.polyEditUV(u=i-20,v=2)
    elif i>=30<40:
        pm.select(allSets[i],r=1,ne=1)
        pm.select(hierarchy=1)
        mel.eval("ConvertSelectionToUVs;")
        pm.polyEditUV(u=i-30,v=3)
