'''created by Yuriy Sivalnev. Its free!!! Totally...i mean it'''

'''
----------------------------------------------------------------------------------------
INSTALLATION: 
    put in is scripts folder(C:\Users\__SOME_NAME__\Documents\maya\2015-x64\scripts)
    ----------------------------------------------------------------------------------------

Type in  Script Editor(in PYTHON tab) to paint or tweak curves:

import ysvCurveTweakerCtx
ysvCurveTweakerCtx.paintCtx('ysvCurveTweaker').run() 

and press CTRL+ENTER

OR for ui to set step for curves CVs:

import ysvCurveTweakerCtx
ysvCurveTweakerCtx.UI().create()


----------------------------------------------------------------------------------------
USAGE:
    CTRL_SHIFT_ALT LMB: unselect selected(you need this to work whis another curve)
        You dont need to select curve whith select tool, tool will work at any curve that is on screen(and project on any poly that is on screen)

    LMB click-drag :
        for paint curve on the virtual plane that has current camera "point of interest" and parallel to view plane
        if start or/and end curve is on top of some poly, cvs will snap to that poly object
    
    Ctrl+LMB click-drag: 
        paint on poly surface(no need to select or make leave!!!!)
      
    Shift+LMB click drag:   
        smooth curve from start click to release mouse button(you just mark cv on which start cmooth operation and end cv - it is NOT      BRUSH)
    
    CTRL+Shift+ LMB: same effect but much stronger
    
    MMB : tweak curve CV that is closest to cursor
    Ctrl MMB: bigger radius(like soft select effect)
    Shift MMB: even bigger radius
    Ctrl Shift MMB: radius that equal crvLen/2
    
    Ctrl Shift Alt MMB: snap curve ends to closest polys(like them is live)
    
I guess thats all, happy tweaking!!!
'''


import maya.cmds as mc

import maya.OpenMaya as om
import maya.OpenMayaUI as omui
import math 
from pymel.core import *
import pymel.core.datatypes as dt
import pymel.core.nodetypes as nt

def getMods():
    mods = getModifiers()

    Ctrl, Alt, Shift, Wnd = 0, 0, 0, 0
    if (mods & 1) > 0: Shift = 1
    if (mods & 4) > 0: Ctrl = 1
    if (mods & 8) > 0: Alt = 1
    if (mods & 16): Wnd = 1

    return Ctrl, Alt, Shift

class UI():
    def __init__(self):
        self.winName = "ysvPaintCurveOnPoly"
        self.winTitle = "Paint curve on poly UI"

    def create(self):
        if not optionVar(ex='ysvPaintCurveStep'):
            optionVar(fv=('ysvPaintCurveStep', 1.0))

        if window(self.winName, exists=True):
            deleteUI(self.winName)
        with window(self.winName, title=self.winTitle):
            with columnLayout():
                stepVal = optionVar(q='ysvPaintCurveStep')
                self.stepSlider = floatSliderGrp(label='Step : ', field=1, columnWidth=(1, 40), min=0, max=1000, fmx=20, value=stepVal, pre=2, cc=Callback(self.setStep))
        showWindow(self.winName)

    def setStep(self):
        value = floatSliderGrp(self.stepSlider, q=1, v=1)
        optionVar(fv=('ysvPaintCurveStep', value))

class baseDraggerCtx():
    def __init__(self, ctxName):
        self.initSel = ls(sl=1)
        
        self.initInViewObjs = getInVewObjs()
        
        liveMeshes = ls(lv=1, dag=1, et=nt.Mesh, ni=1)
        if liveMeshes: self.liveMesh = liveMeshes[0]
        else: self.liveMesh = None
        
        self.ctxName = ctxName
        if draggerContext(self.ctxName, ex=1):
            deleteUI(self.ctxName)                
        
        draggerContext(ctxName, 
                            ppc = self.prePress, pc=self.onPress,
                            dragCommand=self.onDrag,
                            releaseCommand=self.onRelease,
                            finalize=self.finalize, 
                            name = ctxName,
                            cursor='crossHair', undoMode='step')
        
        #print 'context with name {0} created'.format(self.ctxName)

    def prePress(self):
        try:
            self.currCam = PyNode(modelPanel(getPanel(wf=1), q=1, cam=1))
            self.viewDir = self.currCam.viewDirection(space='world')
            self.eyePnt = self.currCam.getEyePoint(space='world')
            self.centerOfInterest = self.currCam.getWorldCenterOfInterest()
        except:
            inViewMessage(msg='error in prePress: Set focus in 3d viewPort', fade=1, fst=300)
        
    def setCursorData(self, xScreen, yScreen):
        self.cursorScreenCoords = (xScreen, yScreen)
        self.cursorWPos, self.cursorWDir = viewToWorld(xScreen, yScreen)
        
    def onPress(self):
        xScreen, yScreen, dummy = draggerContext(self.ctxName, q=1, ap=1)
        self.setCursorData(xScreen, yScreen)
        
        self.btn = draggerContext(self.ctxName, q=1, bu=1)
        self.mods = getMods()
        
    def onHold(self):
        pass
    
    def onDrag(self):
        xScreen, yScreen, dummy = draggerContext(self.ctxName, q=1, dp=1)
        self.setCursorData(xScreen, yScreen)
        
    def onRelease(self):
        pass
    
    def finalize(self):
        pass
    
    def run(self):
        if draggerContext(self.ctxName, ex=1):
            setToolTo(self.ctxName)
            
    def optionsPopupMenu(self):
        pass
    
class paintCtx(baseDraggerCtx):
    def __init__(self, ctxName):
        baseDraggerCtx.__init__(self, ctxName)

        #modelEditor(getPanel(wf=1), e=1, xray=1)
        modelEditor(getPanel(wf=1), e=1, nurbsCurves=1)		

        self.inMeshes = ls(sl=1, dag=1, et=nt.Mesh, ni=1) + ls(lv=1, dag=1, et=nt.Mesh, ni=1)

        if not self.inMeshes:
            self.inMeshes = ls(self.initInViewObjs, dag=1, et=nt.Mesh, ni=1)

        self.meshFns = [mesh.__apimfn__() for mesh in self.inMeshes]

        self.step = optionVar(q='ysvPaintCurveStep')
        print 'in view objs: ', self.initInViewObjs

    def planeIsect(self, planePnt, planeNormal):
        rayLen = 10000
        startL = dt.Point(self.cursorWPos)
        endL = startL+dt.Vector(self.cursorWDir)*rayLen

        return linePlaneIntersect(startL, endL, planePnt, planeNormal)

    def paintOnPress(self):
        self.startScreenWSPos = self.cursorWPos

        pnt = self.planeIsect(self.centerOfInterest, self.viewDir)
        self.crv = curve(p=[pnt])
        self.crv.dispCV.set(1)

        meshes = ls(getInVewObjs(), dag=1, et=nt.Mesh, ni=1)
        self.meshFns = [mesh.__apimfn__() for mesh in meshes]

        self.prevPnt = pnt

    def paintOnDrag(self):
        pnt = self.planeIsect(self.centerOfInterest, self.viewDir)
        if pnt:
            if (pnt - self.prevPnt).length() > self.step:
                curve(self.crv, a=1, p=pnt)
                self.prevPnt = pnt            

    def paintOnRelease(self):
        sPnt = pointPosition(self.crv.cv[0])
        xform(self.crv, sp=sPnt, rp=sPnt, a=1, ws=1)

        self.endScreenWSPos = self.cursorWPos

        crvLen = self.crv.length()

        sCVPos = pointPosition(self.crv.cv[0])    
        eCVPos = pointPosition(self.crv.cv[-1])   

        sMeshHit = closestHitToMeshes(self.meshFns, self.startScreenWSPos, sCVPos - self.startScreenWSPos)
        eMeshHit = closestHitToMeshes(self.meshFns, self.endScreenWSPos, eCVPos - self.endScreenWSPos)


        if sMeshHit:
            move(self.crv, sMeshHit - sCVPos, r=1, ws=1)

        if eMeshHit:
            setToolTo('moveSuperContext')
            softSelect(e=1, sse=1, ssf=1, ssc = '1,0,2,0,1,2', ssd = crvLen/1.3)
            select(self.crv.cv[-1])
            move(eMeshHit, a=1, ws=1)

        select(self.crv)
        self.crv.dispCV.set(0)

        softSelect(e=1, sse=0)
        setToolTo(self.ctxName)

    def paintOnPolyOnPress(self):
        meshHit = closestHitToMeshes(self.meshFns, self.cursorWPos, self.cursorWDir)

        if meshHit:    
            self.paintCrv = curve(p=(meshHit))

            select(self.paintCrv)
            self.paintCrv.dispCV.set(1)

            self.prevHit = meshHit

    def paintOnPolyOnDrag(self):
        meshHit = closestHitToMeshes(self.meshFns, self.cursorWPos, self.cursorWDir)

        try:
            if meshHit and self.paintCrv:
                if (meshHit - self.prevHit).length() > self.step:
                    curve(self.paintCrv, append=1, p=(meshHit))
                    self.prevHit = meshHit
        except: pass


    def getCVNearCursor(self, singleCurve = None):    
        xScr, yScr = self.cursorScreenCoords
        scrPnt = dt.Point(xScr, yScr, 0)

        currView = omui.M3dView.active3dView()

        distances = []
        if singleCurve:
            curves = [singleCurve]
        else:
            curves = self.curves

        for crv in curves:
            for i in range(crv.numCVs()):
                cvPos = pointPosition(crv.cv[i])

                xu, yu = om.MScriptUtil(), om.MScriptUtil()
                xPtr, yPtr = xu.asShortPtr(), yu.asShortPtr()

                mPnt = om.MPoint(cvPos[0], cvPos[1], cvPos[2])
                notClipped = currView.worldToView(mPnt, xPtr, yPtr)

                if notClipped:
                    x = xu.getShort(xPtr)
                    y = yu.getShort(yPtr)

                    crvScrPnt = dt.Point(x, y, 0)
                    dist = (scrPnt - crvScrPnt).length()

                    distances.append([dist, crv, i])

        if distances:
            crv, cvId = min(distances, key = lambda x:x[0])[1:]  
            return crv.cv[cvId]
        else:
            return []

    def smoothOpOnPress(self):
        curves = ls(sl=1, dag=1, et=nt.NurbsCurve, ni=1)

        if not curves:
            self.curves = ls(getInVewObjs(), dag=1, et=nt.NurbsCurve, ni=1)
        else:
            self.curves = curves

        self.startClickCv = self.getCVNearCursor()
        select(self.startClickCv.node().getParent())

    def smoothOpOnRelease(self, iterations):
        crv = self.startClickCv.node()
        self.endClickCv = self.getCVNearCursor(crv)
        #select(self.endClickCv, add=1)

        sId, eId = self.startClickCv.index(), self.endClickCv.index()

        s = min(sId, eId)
        e = max(sId, eId)

        cvs = [cv for cv in crv.cv[s:e]]
        pnts = [pointPosition(cv) for cv in cvs]

        for i in range(iterations):
            smoothCrvPoints(pnts)

        for cv, pnt in zip(cvs, pnts):
            move(cv, pnt, ws=1, a=1)

    def getCVsWeights(self, crv, sId, midId, eId, radiusCount, lockEnds = True):
        maxId = crv.numCVs()
        weights = [0.0]*maxId

        weights[midId] = 1.0

        if radiusCount == 0: 
            if lockEnds:
                weights[0] = 0
                weights[-1] = 0
            return weights

        for i in range(1, radiusCount+1):
            leftId, rightId = midId-i, midId+i
            w = 1.0 - float(i)/(radiusCount+1)        

            if leftId > 0:
                weights[leftId] = w
            if rightId < maxId:
                weights[rightId] = w
        #print weights
        if lockEnds:
            weights[0] = 0
            weights[-1] = 0
        return weights

    def moveOpOnPress(self, radius):
        curves = ls(sl=1, dag=1, et=nt.NurbsCurve, ni=1)

        if not curves:
            self.curves = ls(getInVewObjs(), dag=1, et=nt.NurbsCurve, ni=1)
        else:
            self.curves = curves

        self.startClickCv = self.getCVNearCursor()

        self.crv = self.startClickCv.node()
        select(self.crv.getParent())
        midId = self.startClickCv.index()

        numCVs = self.crv.numCVs()
        if radius == "none":
            radiusCount = 0
        if radius == "short":
            radiusCount = int(numCVs/6)
        if radius == "mid":
            radiusCount = int(numCVs/4)
        if radius == "large":
            radiusCount = int(numCVs/2)

        sId = max(0, midId-radiusCount)
        eId = min(numCVs-1, midId+radiusCount)

        self.cvsToMove = [self.crv.cv[cvId] for cvId in range(sId, eId+1)] #self.crv.cv[sId:eId]
        self.cvsPositions = [pointPosition(cv) for cv in self.cvsToMove]
        self.cvWeights = self.getCVsWeights(self.crv, sId, midId, eId, radiusCount)

        self.midCvWPos = pointPosition(self.startClickCv)

        l0 = self.cursorWPos
        l1 = l0 + self.cursorWDir * (self.midCvWPos - self.cursorWPos).length()*10

        self.startPlaneProjPnt = linePlaneIntersect(l0, l1,  self.midCvWPos, self.cursorWDir)

    def moveOpOnDrag(self): #radius in range (0..numCVs/2)
        l0 = self.cursorWPos
        l1 = l0 + self.cursorWDir * (self.midCvWPos - self.cursorWPos).length()*10

        dragPlaneProjPnt = linePlaneIntersect(l0, l1,   self.midCvWPos, self.cursorWDir)
        offsetVec = dragPlaneProjPnt - self.startPlaneProjPnt

        for cv, pos in zip(self.cvsToMove, self.cvsPositions):
            w = self.cvWeights[cv.index()]

            move(cv, pos+offsetVec*w, ws=1, a=1)


        #x, y = self.cursorScreenCoords
        #print  (x, y)

    def moveEndsOpPress(self):
        curves = ls(sl=1, dag=1, et=nt.NurbsCurve, ni=1)

        if not curves:
            self.curves = ls(getInVewObjs(), dag=1, et=nt.NurbsCurve, ni=1)
        else:
            self.curves = curves

        self.startClickCv = self.getCVNearCursor()
        self.moveEndsCurve = self.startClickCv.node()

        select(self.moveEndsCurve.getParent())

        clickCVId = self.startClickCv.index()

        idChooserList = [ [self.moveEndsCurve.cv[0], clickCVId], [self.moveEndsCurve.cv[-1], self.moveEndsCurve.numCVs()-clickCVId] ]

        self.closestCrvEnd = min(idChooserList, key = lambda x:x[1])[0]

        #select(self.closestCrvEnd)

        numCVs = self.moveEndsCurve.numCVs()
        radiusCount = int(numCVs/1.3)

        midId = self.closestCrvEnd.index()
        sId = max(0, midId-radiusCount)
        eId = min(numCVs-1, midId+radiusCount)

        self.cvsToMove = [self.moveEndsCurve.cv[cvId] for cvId in range(sId, eId+1)] #self.crv.cv[sId:eId]
        self.cvsPositions = [pointPosition(cv) for cv in self.cvsToMove]
        self.cvWeights = self.getCVsWeights(self.moveEndsCurve, sId, midId, eId, radiusCount, False)

        self.midCvWPos = pointPosition(self.startClickCv)

        l0 = self.cursorWPos
        l1 = l0 + self.cursorWDir * (self.midCvWPos - self.cursorWPos).length()*10

        self.startPlaneProjPnt = linePlaneIntersect(l0, l1,  self.midCvWPos, self.cursorWDir)        

    def moveEndsOpDrag(self):
        meshHit = closestHitToMeshes(self.meshFns, self.cursorWPos, self.cursorWDir)

        if meshHit:
            offsetVec = meshHit - self.midCvWPos
        else:
            l0 = self.cursorWPos
            l1 = l0 + self.cursorWDir * (self.midCvWPos - self.cursorWPos).length()*10

            dragPlaneProjPnt = linePlaneIntersect(l0, l1,   self.midCvWPos, self.cursorWDir)
            offsetVec = dragPlaneProjPnt - self.startPlaneProjPnt

        for cv, pos in zip(self.cvsToMove, self.cvsPositions):
            w = self.cvWeights[cv.index()]

            move(cv, pos+offsetVec*w, ws=1, a=1)

    def moveEndsOpRelease(self):
        select(self.moveEndsCurve)


    def onPress(self):
        baseDraggerCtx.onPress(self)
        cntrl, alt, shift = self.mods

        if self.btn ==1:
            if not cntrl and not alt and not shift:
                self.paintOnPress()

            elif shift and not alt:
                self.smoothOpOnPress() 

            elif cntrl and not shift and not alt:
                self.paintOnPolyOnPress()	

            elif cntrl and shift and alt:
                select(cl=1)

        elif self.btn==2:
            if not cntrl and not shift and not alt:
                self.moveOpOnPress('none')
            elif cntrl and not shift and not alt:
                self.moveOpOnPress('short')
            elif not cntrl and shift and not alt:
                self.moveOpOnPress('mid')
            elif cntrl and shift and not alt:
                self.moveOpOnPress('large')	

            elif cntrl and shift and alt:
                self.moveEndsOpPress()

    def onDrag(self):
        baseDraggerCtx.onDrag(self)

        cntrl, alt, shift = self.mods
        if self.btn ==1:
            if not cntrl and not alt and not shift:
                self.paintOnDrag()
            elif cntrl and not shift and not alt:
                self.paintOnPolyOnDrag()

            #curve(self.crv, append=1, p=[pnt])
        elif self.btn==2:
            if not cntrl and not shift and not alt:
                self.moveOpOnDrag()
            elif cntrl and not shift and not alt:
                self.moveOpOnDrag()
            elif cntrl and shift and not alt:
                self.moveOpOnDrag()
            elif not cntrl and shift and not alt:
                self.moveOpOnDrag()

            elif cntrl and shift and alt:
                self.moveEndsOpDrag()            


        mc.refresh(cv=True)

    def onRelease(self):
        #baseDraggerCtx.onRelease(self)

        cntrl, alt, shift = self.mods
        if self.btn == 1:
            if not cntrl and not shift and not alt:
                self.paintOnRelease()

            elif shift and not cntrl and not alt:
                self.smoothOpOnRelease(1)

            elif shift and cntrl and not alt:
                self.smoothOpOnRelease(7)
        elif self.btn ==2:
            if cntrl and shift and alt:
                self.moveEndsOpRelease()             

            #elif not shift and cntrl:
                #self.smoothOpOnRelease(7)
        try: self.paintCrv.dispCV.set(0)
        except: pass

    def finalize(self):
        #baseDraggerCtx.finalize(self)
        #modelEditor(getPanel(wf=1), e=1, xray=0) 
        pass

    def run(self):
        baseDraggerCtx.run(self)


def getMods():
    mods = getModifiers()

    Ctrl, Alt, Shift, Wnd = 0, 0, 0, 0
    if (mods & 1) > 0: Shift = 1
    if (mods & 4) > 0: Ctrl = 1
    if (mods & 8) > 0: Alt = 1
    if (mods & 16): Wnd = 1

    return Ctrl, Alt, Shift

def selectFromScreen():
    select(cl=1)
    try:
        activeView = omui.M3dView.active3dView()
        om.MGlobal.selectFromScreen(0,0,activeView.portWidth(),activeView.portHeight(),om.MGlobal.kReplaceList)
    except:
        inViewMessage(msg='Failed to select from screen(in ysvUtils.py)', fade=1, fst=500, pos='midCenter')

def getInVewObjs():
    sel = ls(sl=1)
    select(cl=1)

    selectMode(o=1)
    hilite(ls(hl=1), u=1)

    try:
        activeView = omui.M3dView.active3dView()
        om.MGlobal.selectFromScreen(0,0,activeView.portWidth(),activeView.portHeight(),om.MGlobal.kReplaceList)
    except:
        inViewMessage(msg='Failed to select from screen', fade=1, fst=500, pos='midCenter')    

    result = ls(sl=1)
    select(sel)
    return result

def viewToWorld(xScreen, yScreen):
    pnt, vec = om.MPoint(), om.MVector()

    try: omui.M3dView().active3dView().viewToWorld(
        int(xScreen), int(yScreen), pnt, vec)
    except: pass

    return dt.Point(pnt), dt.Vector(vec)

def getEulerRotationQuaternion(normal, upvector):
    '''
    returns the x,y,z degree angle rotation corresponding to a direction vector
    input: upvector (MVector) & normal (MVector)
    '''
    upvector = om.MVector (upvector[0], upvector[1], upvector[2])
    normalvector = om.MVector(normal[0], normal[1], normal[2])
    quat = om.MQuaternion(upvector, normalvector)
    quatAsEuler = quat.asEulerRotation()

    return math.degrees(quatAsEuler.x), math.degrees(quatAsEuler.y), math.degrees(quatAsEuler.z)

def getCurrCam():
    try:return PyNode(modelPanel(getPanel(wf=1), q=1, cam=1))
    except:return None

def meshIntersect(meshFn, inPos, inDir):
    # inMesh object
    pos = om.MFloatPoint(inPos[0], inPos[1], inPos[2])
    rayDir = om.MFloatVector(inDir[0], inDir[1], inDir[2])

    hitPnt = om.MFloatPoint()  # intersection
    hitFace = om.MScriptUtil()
    hitTri = om.MScriptUtil()
    hitFace.createFromInt(0)
    hitTri.createFromInt(0)

    hFacePtr = hitFace.asIntPtr()
    hTriPtr = hitTri.asIntPtr()

    farclip = getCurrCam().getFarClipPlane()
    # print 'getting intersection ', 
    try:
        hit = meshFn.closestIntersection(pos,  # RaySource,
                                         rayDir,  # rayDirection
                                         None,  # faceIds
                                         None,  # triIds
                                         True,  # idsSorted
                                         om.MSpace.kWorld,  # space
                                         farclip,  # maxParam
                                         True,  # testBothDirections
                                         None,  # accelParams
                                         hitPnt,  # hitPoint
                                         None,  # hitRayParam      
                                         hFacePtr,  # hitFace
                                         hTriPtr,  # hitTriangle
                                         None,  # hitBary1
                                         None)  # hitBary2
    except:
        print 'ERROR: hit failed'
        # raise

    return hit, hitPnt  # , hitFace.getInt(hFacePtr), hitTri.getInt(hTriPtr)

def closestHitToMeshes(meshFns, inPos, inDir):
    meshHits = []
    for meshFn in meshFns:
        state, hit = meshIntersect(meshFn, inPos, inDir)
        if state:
            dist = (dt.Point(hit) - inPos).length()
            meshHits.append([dist, dt.Point(hit)])

    if meshHits:    
        return min(meshHits, key = lambda x: x[0])[1]   
    else:
        return False
    
def linePlaneIntersect(linePnt0, linePnt1, planePnt, planeNormal, epsilon=0.00001):
    lineNormal = linePnt1 - linePnt0
    w = linePnt0 - planePnt
    dot = planeNormal.dot(lineNormal)
    if abs(dot) > epsilon:
        factor = -planeNormal.dot(w)/dot
        return linePnt0 + (linePnt1-linePnt0)*factor
    else:
        # The segment is parallel to plane
        return None
    
def smoothCrvPoints(points):
    for i in range(1, len(points)-1):
        points[i]  = points[i] * 0.4 + (points[i+1] + points[i-1]) * 0.3
