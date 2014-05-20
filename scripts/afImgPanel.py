import pymel.core as pm
import pymel.all as pa

imgOp = 0.3
imgDep = 10

#get current camera
curCam = pm.modelPanel(pm.getPanel(wf=True),q=True,cam=True)
#select image and creat imagePlane and setup
fileNm = pm.fileDialog2(ds=0,fm=1,cap='open',okc='Select Image')
ImgPln = pm.imagePlane(fn=fileNm[0],lookThrough=curCam,maintainRatio=1)
pm.setAttr(ImgPln[1]+'.displayOnlyIfCurrent',True)
pm.setAttr(ImgPln[0]+'.translateZ',-pm.getAttr(curCam+'.translateZ')/3+-imgDep)
pm.setAttr(ImgPln[1]+'.alphaGain',imgOp)
pm.setAttr(ImgPln[1]+'.textureFilter',1)

#aligh to the camera
#create locator to be the parent and then create parent constraint
pLoc = pm.spaceLocator()
pm.parent(ImgPln[0],pLoc)
pm.parentConstraint(curCam,pLoc)

#Toggle image plane visibility
if(pm.getAttr(ImgPln[1]+'.visibility')):
    pm.setAttr(ImgPln[1]+'.visibility',0)
else:
    pm.setAttr(ImgPln[1]+'.visibility',1)
