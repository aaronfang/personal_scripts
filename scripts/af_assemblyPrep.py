import pymel.core as pm
# Step1:
# Select top group node. Run the following.It will generate a locator.
# Send to the current group pivot position.
# You can position the locator where you want to represent the final pivot position.
curSel = pm.ls(sl=True,type='transform')
trans = pm.xform(curSel[0],ws=1,piv=1,q=1)
rot = pm.xform(curSel[0],ws=1,ro=1,q=1)
scl = pm.xform(curSel[0],ws=1,s=1,q=1)
locNd = pm.spaceLocator(n=(curSel[0]+'_LOC'),p=(0,0,0))
pm.xform(locNd,s=scl,t=(trans[0],trans[1],trans[2]),ro=rot)
# Manually trans/rot the locator to the place of the final pivot.

#step2:
# Parent the top group to the locator.
# Add attribute to store the trans/rot/scale information.
transLoc = pm.xform(locNd,ws=1,piv=1,q=1)
rotLoc = pm.xform(locNd,ws=1,ro=1,q=1)
sclLoc = pm.xform(locNd,ws=1,s=1,q=1)

pm.parent(curSel[0],locNd)

pm.addAttr(locNd,ln='trans_info',at='double3')
pm.addAttr(locNd,p='trans_info',ln='trans_infoX',at='double')
pm.addAttr(locNd,p='trans_info',ln='trans_infoY',at='double')
pm.addAttr(locNd,p='trans_info',ln='trans_infoZ',at='double')
pm.setAttr((locNd+'.trans_info'),transLoc[0:3],type='double3')

pm.addAttr(locNd,ln='rot_info',at='double3')
pm.addAttr(locNd,p='rot_info',ln='rot_infoX',at='double')
pm.addAttr(locNd,p='rot_info',ln='rot_infoY',at='double')
pm.addAttr(locNd,p='rot_info',ln='rot_infoZ',at='double')
pm.setAttr((locNd+'.rot_info'),rotLoc,type='double3')

pm.addAttr(locNd,ln='scal_info',at='double3')
pm.addAttr(locNd,p='scal_info',ln='scale_infoX',at='double')
pm.addAttr(locNd,p='scal_info',ln='scale_infoY',at='double')
pm.addAttr(locNd,p='scal_info',ln='scale_infoZ',at='double')
pm.setAttr((locNd+'.scal_info'),sclLoc,type='double3')

