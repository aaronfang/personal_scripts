import pymel.core as pm
# Step1:
# Select top group node. Run the following.It will generate a locator.
# Send to the current group pivot position.
# You can position the locator where you want to represent the final pivot position.
curSel = pm.ls(sl=True,type='transform')[0]
trans = pm.xform(curSel,ws=1,piv=1,q=1)
rot = pm.xform(curSel,ws=1,ro=1,q=1)
scl = pm.xform(curSel,ws=1,s=1,q=1)
gpNd = pm.group(n=(curSel+'_GRP'),em=1)
pm.xform(gpNd,s=scl,t=trans[0:3],ro=rot)
# Manually trans/rot the locator to the place of the final pivot.

#step2:
# Parent the top group to the locator.
# Add attribute to store the trans/rot/scale information.
transGrp = pm.xform(gpNd,ws=1,piv=1,q=1)
rotGrp = pm.xform(gpNd,ws=1,ro=1,q=1)
sclGrp = pm.xform(gpNd,ws=1,s=1,q=1)
transVal = pm.xform(gpNd,ws=1,t=1,q=1)

pm.parent(curSel,gpNd)

pm.addAttr(gpNd,ln='trans_info',at='double3')
pm.addAttr(gpNd,p='trans_info',ln='trans_infoX',at='double')
pm.addAttr(gpNd,p='trans_info',ln='trans_infoY',at='double')
pm.addAttr(gpNd,p='trans_info',ln='trans_infoZ',at='double')
pm.setAttr((gpNd+'.trans_info'),transGrp[0:3],type='double3')

pm.addAttr(gpNd,ln='rot_info',at='double3')
pm.addAttr(gpNd,p='rot_info',ln='rot_infoX',at='double')
pm.addAttr(gpNd,p='rot_info',ln='rot_infoY',at='double')
pm.addAttr(gpNd,p='rot_info',ln='rot_infoZ',at='double')
pm.setAttr((gpNd+'.rot_info'),rotGrp,type='double3')

pm.addAttr(gpNd,ln='scal_info',at='double3')
pm.addAttr(gpNd,p='scal_info',ln='scale_infoX',at='double')
pm.addAttr(gpNd,p='scal_info',ln='scale_infoY',at='double')
pm.addAttr(gpNd,p='scal_info',ln='scale_infoZ',at='double')
pm.setAttr((gpNd+'.scal_info'),sclGrp,type='double3')

# Move Grp to the origin and Freeze Transform. Then move it back to where it was,
# With the right xform info.
pm.xform(gpNd,ws=1,t=(transVal[0]-transGrp[0],transVal[1]-transGrp[1],transVal[2]-transGrp[2]))
pm.xform(gpNd,r=1,ro=(-rotGrp[0],-rotGrp[1],-rotGrp[2]))
pm.xform(gpNd,r=1,s=(1/sclGrp[0],1/sclGrp[1],1/sclGrp[2]))

pm.makeIdentity(apply=1,t=1,r=1,s=1,n=0,pn=0)

pm.xform(gpNd,ws=1,t=(transGrp[0],transGrp[1],transGrp[2]))
pm.xform(gpNd,r=1,ro=(rotGrp[0],rotGrp[1],rotGrp[2]))
pm.xform(gpNd,r=1,s=(sclGrp[0],sclGrp[1],sclGrp[2]))
