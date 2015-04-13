# rename shading group name to material name but with SG ended
import pymel.core as pm
import re
selSG = pm.ls(sl=True,fl=True)
for SG in selSG:
    curMat = pm.listConnections(SG,d=1)
    for mat in curMat:
        if pm.nodeType(mat) == 'blinn' or pm.nodeType(mat) == 'lambert':
            sgNM = re.split("_mat",str(mat))[0]+"SG"
            pm.rename(SG,sgNM)
