import pymel.core as pm

# Select top group node. Run the following.It will generate a locator.
# Send to the current group pivot position.
# You can position the locator where you want to represent the final pivot position.
curSel = pm.ls(sl=True,type='transform')
trans = pm.xform(curSel[0],ws=1,piv=1,q=1)
rot = pm.xform(curSel,ws=1,ro=1,q=1)
scl = pm.xform(curSel,ws=1,s=1,q=1)
locNd = pm.spaceLocator(n=(curSel[0]+'_LOC'),p=(0,0,0))
pm.xform(locNd,s=scl,t=(trans[0],trans[1],trans[2]),ro=rot)

# Parent the top group to the locator.
# Add attribute to store the trans/rot/scale information.
pm.parent(curSel[0],locNd)
pm.addAttr(locNd,ln='scal_info',at='double3')
pm.addAttr(locNd,p='scal_info',ln='scale_infoX',at='double')
pm.addAttr(locNd,p='scal_info',ln='scale_infoY',at='double')
pm.addAttr(locNd,p='scal_info',ln='scale_infoZ',at='double')
pm.setAttr((locNd+'.scal_info'),0,0,0,type='double3')
