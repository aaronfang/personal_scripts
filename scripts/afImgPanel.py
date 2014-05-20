import pymel.core as pm
import pymel.all as pa

#variables
imgOp = 1
imgDep = 0
curCam = ''
ImgPln = []
fileNm = ''
pLoc = ''
bmCam = curCam





#create image plane and set up some attrs
def createImgPln():
    global imgOp
    global imgDep
    global curCam
    global ImgPln
    global fileNm
    global pLoc

    #comfirmDialog for checking if ImgPln in the scene
    allTransNd = pm.ls(type='transform',fl=True)
    isImgPln = []
    for trans in allTransNd:
        if trans == 'ImagePlane_Parent_Loc':
            isImgPln.append(trans)
    if len(isImgPln) >= 1:
        cfmAnswer = pm.confirmDialog( title='Confirm', message='Delete Image Plane?', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
        if cfmAnswer == 'Yes':
            cleanupImgPln()
            createImgPln()
    elif len(isImgPln) == 0:
        #image plane opacty and offset from camera
        imgOp = 1
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
        LocCons = pm.parentConstraint(curCam,pLoc)
        pm.setAttr(pLoc+'Shape.template',1)
        pm.setAttr(LocCons+'.template',1)

#Toggle image plane visibility
def imgPlnVisTgl():
    #comfirmDialog for checking if ImgPln in the scene
    allTransNd = pm.ls(type='transform',fl=True)
    isImgPln = []
    for trans in allTransNd:
        if trans == 'ImagePlane_Parent_Loc':
            isImgPln.append(trans)
    if len(isImgPln) == 0:
        cfmAnswer = pm.confirmDialog( title='Confirm', message='Create New Image Plane?', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
        if cfmAnswer == 'Yes':
            createImgPln()
    elif len(isImgPln) >= 1:
        if(pm.getAttr(ImgPln[1]+'.visibility')):
            pm.setAttr(ImgPln[1]+'.visibility',0)
            pm.select(ImgPln[0],d=True)
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
        addImgBookMark()

#Select image plane
def selImgPln():
    #comfirmDialog for checking if ImgPln in the scene
    allTransNd = pm.ls(type='transform',fl=True)
    isImgPln = []
    for trans in allTransNd:
        if trans == 'ImagePlane_Parent_Loc':
            isImgPln.append(trans)
    if len(isImgPln) == 0:
        cfmAnswer = pm.confirmDialog( title='Confirm', message='Create New Image Plane?', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
        if cfmAnswer == 'Yes':
            createImgPln()
    elif len(isImgPln) >= 1:
        pm.select(ImgPln[0],r=True)
        if(pm.getAttr(ImgPln[0]+'.t',lock=True)):
            pm.setAttr(ImgPln[0]+'.t',lock=False)
            pm.setAttr(ImgPln[0]+'.r',lock=False)
            pm.setAttr(ImgPln[0]+'.s',lock=False)
            pm.toggle(ImgPln[0],state=False,template=True)

#Lock the image plane
def imgPlnLock():
    #comfirmDialog for checking if ImgPln in the scene
    allTransNd = pm.ls(type='transform',fl=True)
    isImgPln = []
    for trans in allTransNd:
        if trans == 'ImagePlane_Parent_Loc':
            isImgPln.append(trans)
    if len(isImgPln) == 0:
        cfmAnswer = pm.confirmDialog( title='Confirm', message='Create New Image Plane?', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
        if cfmAnswer == 'Yes':
            createImgPln()
    elif len(isImgPln) >= 1:
        if(pm.getAttr(ImgPln[0]+'.t',lock=False)):
            pm.setAttr(ImgPln[0]+'.t',lock=True)
            pm.setAttr(ImgPln[0]+'.r',lock=True)
            pm.setAttr(ImgPln[0]+'.s',lock=True)
            pm.toggle(ImgPln[0],state=True,template=True)
            pm.select(ImgPln,d=True)

#remove image plane and cleanup
def cleanupImgPln():
    #comfirmDialog for checking if ImgPln in the scene
    allTransNd = pm.ls(type='transform',fl=True)
    isImgPln = []
    for trans in allTransNd:
        if trans == 'ImagePlane_Parent_Loc':
            isImgPln.append(trans)
    if len(isImgPln) == 0:
        cfmAnswer = pm.confirmDialog( title='Confirm', message='Create New Image Plane?', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
        if cfmAnswer == 'Yes':
            createImgPln()
    elif len(isImgPln) >= 1:
        pm.delete(pLoc)
    #unlock the camera
    if(pm.getAttr(curCam+'.t',lock=True)):
        pm.setAttr(curCam+'.t',lock=False)
        pm.setAttr(curCam+'.r',lock=False)
    #remove current bookmark
    cmvList = pm.ls(type='cameraView')
    if len(cmvList)!=0:
        for cmv in cmvList:
            if cmv == 'imageView_bookmark':
                pm.cameraView(cmv,c=bmCam,e=True,rb=True)
                pm.delete(cmv)

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
    cmvList = pm.ls(type='cameraView')
    if len(cmvList)==0:
        cfmAnswer = pm.confirmDialog( title='Confirm', message='Create New Bookmark?', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
        if cfmAnswer == 'Yes':
            addImgBookMark()
    else:
        pm.cameraView('imageView_bookmark',e=True,c=bmCam,setCamera=True)


#add switch to the Image Plane transparency
def imgPlnOpSw():
    #comfirmDialog for checking if ImgPln in the scene
    allTransNd = pm.ls(type='transform',fl=True)
    isImgPln = []
    for trans in allTransNd:
        if trans == 'ImagePlane_Parent_Loc':
            isImgPln.append(trans)
    if len(isImgPln) == 0:
        cfmAnswer = pm.confirmDialog( title='Confirm', message='Create New Image Plane?', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
        if cfmAnswer == 'Yes':
            createImgPln()
    elif len(isImgPln) >= 1:
        if pm.getAttr(ImgPln[1]+'.alphaGain') == 1:
            pm.setAttr(ImgPln[1]+'.alphaGain', 0.7)
        elif pm.getAttr(ImgPln[1]+'.alphaGain') == 0.7:
            pm.setAttr(ImgPln[1]+'.alphaGain', 0.5)
        elif pm.getAttr(ImgPln[1]+'.alphaGain') == 0.5:
            pm.setAttr(ImgPln[1]+'.alphaGain', 0.3)
        elif pm.getAttr(ImgPln[1]+'.alphaGain') == 0.3:
            pm.setAttr(ImgPln[1]+'.alphaGain', 0.08)
        elif pm.getAttr(ImgPln[1]+'.alphaGain') == 0.08:
            pm.setAttr(ImgPln[1]+'.alphaGain', 1)

#Imgae Plane depth trans
def transImgPlnDp():
    #comfirmDialog for checking if ImgPln in the scene
    allTransNd = pm.ls(type='transform',fl=True)
    isImgPln = []
    for trans in allTransNd:
        if trans == 'ImagePlane_Parent_Loc':
            isImgPln.append(trans)
    if len(isImgPln) == 0:
        cfmAnswer = pm.confirmDialog( title='Confirm', message='Create New Image Plane?', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
        if cfmAnswer == 'Yes':
            createImgPln()
    elif len(isImgPln) >= 1:
        camDp = pm.getAttr(curCam+'.translateZ')
        imgPlnScale = pm.getAttr(ImgPln[0]+'.s')
        if pm.getAttr(ImgPln[0]+'.translateZ') == (camDp)*0.01:
            pm.setAttr(ImgPln[0]+'.translateX',0)
            pm.setAttr(ImgPln[0]+'.translateY',0)
            pm.setAttr(ImgPln[0]+'.translateZ',(camDp)*0.1)
            pm.setAttr(ImgPln[0]+'.s',1,1,1)
        elif pm.getAttr(ImgPln[0]+'.translateZ') == (camDp)*0.1:
            pm.setAttr(ImgPln[0]+'.translateX',0)
            pm.setAttr(ImgPln[0]+'.translateY',0)
            pm.setAttr(ImgPln[0]+'.translateZ',(camDp)*0.01)
            pm.setAttr(ImgPln[0]+'.s',0.2,0.2,0.2)
        else:
            pm.setAttr(ImgPln[0]+'.translateX',0)
            pm.setAttr(ImgPln[0]+'.translateY',0)
            pm.setAttr(ImgPln[0]+'.translateZ',(camDp)*0.1)
            pm.setAttr(ImgPln[0]+'.s',1,1,1)
    
#HUD

#change image file
def changeImgFile():
    #comfirmDialog for checking if ImgPln in the scene
    allTransNd = pm.ls(type='transform',fl=True)
    isImgPln = []
    for trans in allTransNd:
        if trans == 'ImagePlane_Parent_Loc':
            isImgPln.append(trans)
    if len(isImgPln) == 0:
        cfmAnswer = pm.confirmDialog( title='Confirm', message='Create New Image Plane?', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
        if cfmAnswer == 'Yes':
            createImgPln()
    elif len(isImgPln) >= 1:
        pa.mel.eval('AEimagePlaneBrowser "AEassignImageCB imagePlaneShape1.type imagePlaneShape1.imageName" imagePlaneShape1')
        pm.setAttr(ImgPln[0]+'.translateX',0)
        pm.setAttr(ImgPln[0]+'.translateY',0)




#More Image Planes to the camera






