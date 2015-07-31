# ------------------------------------------
# af_prepGrpA.py
# Summary: This script allows user to relocate the pivot point of a asset.
# 1, Make outliner structure as famity name.
# 2, Select the group node in asset level.
# 3, Run the following script.

import pymel.core as pm
import maya.mel as mm

# add '_grp' to the top node
curSel = pm.ls(sl=True,type='transform')[0]
newNm = curSel + '_grp'
pm.rename(curSel,newNm)

# center pivot
mm.eval('CenterPivot')

# freeze transform
import pymel.core as pm
pm.makeIdentity(apply=1,t=1,r=1,s=1,n=0,pn=0)

# grouping
assetNm = curSel.split('_')[0]
trans = pm.xform(curSel,ws=1,piv=1,q=1)
rot = pm.xform(curSel,ws=1,ro=1,q=1)
scl = pm.xform(curSel,ws=1,s=1,q=1)
gpNd = pm.group(n=assetNm,em=1)
pm.xform(gpNd,s=scl,t=trans[0:3],ro=rot)

# display local rotation axis
mm.eval('ToggleLocalRotationAxes')

# isolate assets
pm.select(curSel,add=1)
mm.eval('$currentPanel = `getPanel -withFocus`;enableIsolateSelect $currentPanel true;')
mm.eval('fitPanel -selected')
pm.select(gpNd,r=1)



# ------------------------------------------
# af_prepGrpB.py
# Summary: This script parent pivot group back to the assets structure.

# get the parent node of the curSel Asset
prtNd = pm.listRelatives(curSel,p=1)
pm.parent(gpNd,prtNd)
pm.parent(curSel,gpNd)
mm.eval('$currentPanel = `getPanel -withFocus`;enableIsolateSelect $currentPanel false;')
pm.select(gpNd,r=1)
'''
tGrp = pm.xform(gpNd,ws=1,piv=1,q=1)[0:3]
rGrp = pm.xform(gpNd,ws=1,ro=1,q=1)
sGrp = pm.xform(gpNd,ws=1,s=1,q=1)
pm.xform(gpNd,s=(1,1,1),t=(0,0,0),ro=(0,0,0))
resp = pm.confirmDialog(t='Preview',m='Put it back!',b='Yes')
if resp == 'Yes':pm.xform(gpNd,s=sGrp,t=tGrp,ro=rGrp)
'''
