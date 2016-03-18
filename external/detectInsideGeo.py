import maya.OpenMaya as OM
from math import fmod

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

from pymel.core import *


def testIntersect():
    sel = ls(sl=1)
    container = sel[0]
    checkInsideObj = sel[1]  
    
    allVtx = ls(str(checkInsideObj)+'.vtx[*]',fl=1)
    allIn = []
    start = timerX()
    
    for eachVtx in allVtx:
      location = pointPosition(eachVtx,w=1)
      test = pyRayIntersect(container,location,(0,1,0))
      if(test):
          allIn.append(eachVtx)
          
    elapsedTime = timerX(startTime = start)
    print "time :",elapsedTime
    select(allIn,replace=1)