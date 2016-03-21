import maya.OpenMaya as OM
import maya.OpenMayaUI as OMU
from math import fmod
import maya.cmds as cmds


def pyRayIntersect(mesh, point, direction=(0.0, 1.0, 0.0)):
    OM.MGlobal.selectByName(mesh,OM.MGlobal.kReplaceList)
    sList = OM.MSelectionList()
    #Assign current selection to the selection list object
    OM.MGlobal.getActiveSelectionList(sList)

    item = OM.MDagPath()
    sList.getDagPath(0, item)
    item.extendToShape()

    fnMesh = OM.MFnMesh(item)
    raySource = OM.MFloatPoint(point[0], point[1], point[2], 1.0)
    rayDir = OM.MFloatVector(direction[0], direction[1], direction[2])
    faceIds = None
    triIds = None
    idsSorted = False
    testBothDirections = False
    worldSpace = OM.MSpace.kWorld
    maxParam = 999999
    accelParams = None
    sortHits = True
    hitPoints = OM.MFloatPointArray()
    #hitRayParams = OM.MScriptUtil().asFloatPtr()
    hitRayParams = OM.MFloatArray()
    hitFaces = OM.MIntArray()
    hitTris = None
    hitBarys1 = None
    hitBarys2 = None
    tolerance = 0.0001
    hit = fnMesh.allIntersections(raySource, rayDir, faceIds, triIds, idsSorted, worldSpace, maxParam, testBothDirections, accelParams, sortHits, hitPoints, hitRayParams, hitFaces, hitTris, hitBarys1, hitBarys2, tolerance)

    result = int(fmod(len(hitFaces), 2))

    #clear selection as may cause problem if the function is called multiple times in succession
    #OM.MGlobal.clearSelectionList()
    return result


# test

sel = cmds.ls(sl=True,fl=True)
container = sel[0]
checkInsideObj = sel[1]

allVtx = cmds.ls('{0}.vtx[:]'.format(checkInsideObj),fl=True)
allIn = []
start = cmds.timerX()

for vtx in allVtx:
  location = cmds.pointPosition(vtx,w=True)
  test = pyRayIntersect(container,location,(0,1,0))
  if(test):
      allIn.append(vtx)

elapsedTime = cmds.timerX(startTime = start)
print "time :",elapsedTime

inner_faces = cmds.polyListComponentConversion(allIn,fv=True,tf=True)


# select faces that facing the camera
# 1. Select your mesh and switch to component mode of face selection (RMB on the object and select face from the popup).
# 2. From the menu: Display> polygons> backface culling.
# 3. Run the following python
cmds.select(checkInsideObj,r=True)


view = OMU.M3dView.active3dView()
OM.MGlobal.selectFromScreen(0, 0, view.portWidth(), view.portHeight(), OM.MGlobal.kReplaceList)