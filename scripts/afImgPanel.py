import pymel.core as pm

imgOp = 0
imgDep = 0
curCam = ''
ImgPln = []
fileNm = ''
pLoc = ''
bmCam = ''
#create image plane and set up some attrs
def createImgPln():
    global imgOp
    global imgDep
    global curCam
    global ImgPln
    global fileNm
    global pLoc
    #image plane opacty and offset from camera
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
    pLoc = pm.spaceLocator(name='ImagePlane_Parent_Loc')
    pm.parent(ImgPln[0],pLoc)
    pm.parentConstraint(curCam,pLoc)

#Toggle image plane visibility
def imgPlnVisTgl():
    if(pm.getAttr(ImgPln[1]+'.visibility')):
        pm.setAttr(ImgPln[1]+'.visibility',0)
    else:
        pm.setAttr(ImgPln[1]+'.visibility',1)

#Toggle lock current camera
def camLockTgl():
    if(pm.getAttr(curCam+'.t',lock=True)):
        pm.setAttr(curCam+'.t',lock=False)
        pm.setAttr(curCam+'.r',lock=False)
    else:
        pm.setAttr(curCam+'.t',lock=True)
        pm.setAttr(curCam+'.r',lock=True)

#Select image plane
def selImgPln():
    pm.select(ImgPln[0],r=True)

#Toggle lock image plane's translate rotate and scale
def imgPlnLockTgl():
    if(pm.getAttr(ImgPln[0]+'.t',lock=True)):
        pm.setAttr(ImgPln[0]+'.t',lock=False)
        pm.setAttr(ImgPln[0]+'.r',lock=False)
        pm.setAttr(ImgPln[0]+'.s',lock=False)
        pm.toggle(ImgPln[0],state=False,template=True)
    else:
        pm.setAttr(ImgPln[0]+'.t',lock=True)
        pm.setAttr(ImgPln[0]+'.r',lock=True)
        pm.setAttr(ImgPln[0]+'.s',lock=True)
        pm.toggle(ImgPln[0],state=True,template=True)

#remove image plane and cleanup
def cleanupImgPln():
    pm.delete(pLoc)



#bookmark camera position
def addImgBookMark():
    global bmCam
    bmCam = pm.modelPanel(pm.getPanel(wf=True),q=True,cam=True)
    #remove current bookmark
    cmvList = pm.ls(type='cameraView')
    if len(cmvList)!=0:
        for cmv in cmvList:
            if cmv == 'imageView_bookmark':
                pm.cameraView(cmv,c=bmCam,e=True,rb=True)
                pm.delete(cmv)
    #add bookmark
    addBM = pm.cameraView(c=bmCam,ab=True,n='imageView_bookmark')

#Restore from bookmark
def restoreImgBM():
    pm.cameraView('imageView_bookmark',e=True,c=bmCam,setCamera=True)





