import maya.OpenMaya as OM
import maya.OpenMayaUI as OMU
from math import fmod
import maya.cmds as cmds


def cameraFrustum_build(cam_shape):
    #make sure a camera is loaded
    if cam_shape==0:
        cmds.error('no camera loaded...select a camera and load')
    else:
    #create frustum only if one doesnt already exist
        selCamXform = cmds.listRelatives(cam_shape[0], p=1)
        prefix = 'frust_'
        frustumGrpName = prefix + 'camera_frustum_all_grp'
        if cmds.objExists(frustumGrpName)==0:
        #create main grp
            frustumMainGrp = cmds.group(em=1, n=frustumGrpName);
            cmds.setAttr(frustumGrpName + '.tx', lock=1, keyable=0, channelBox=0)
            cmds.setAttr(frustumGrpName + '.ty', lock=1, keyable=0, channelBox=0)
            cmds.setAttr(frustumGrpName + '.tz', lock=1, keyable=0, channelBox=0)
            cmds.setAttr(frustumGrpName + '.rx', lock=1, keyable=0, channelBox=0)
            cmds.setAttr(frustumGrpName + '.ry', lock=1, keyable=0, channelBox=0)
            cmds.setAttr(frustumGrpName + '.rz', lock=1, keyable=0, channelBox=0)
            cmds.setAttr(frustumGrpName + '.sx', lock=1, keyable=0, channelBox=0)
            cmds.setAttr(frustumGrpName + '.sy', lock=1, keyable=0, channelBox=0)
            cmds.setAttr(frustumGrpName + '.sz', lock=1, keyable=0, channelBox=0)
            cmds.setAttr(frustumGrpName + '.v', lock=1, keyable=0, channelBox=0)

        #create frustum geo
            frustumGeo = cmds.polyCube(w=2, h=2, d=2, n=prefix + 'camera_frustum_geo')
            cmds.delete(frustumGeo[0], constructionHistory=True)
            cmds.parent(frustumGeo[0], frustumMainGrp)
            
        #load plugin "nearestPointOnMesh.mll" if needed and connect 
            plugin = cmds.pluginInfo('nearestPointOnMesh.mll', q=1, l=1)
            if plugin==0:
                cmds.loadPlugin('nearestPointOnMesh.mll')

            nearNodeName = prefix + 'npomNode'  
            npomNode = cmds.createNode('nearestPointOnMesh', n=nearNodeName)
            cmds.connectAttr(frustumGeo[0] + '.worldMesh', npomNode + '.inMesh')        

        #create clusters
            cmds.select(frustumGeo[0] + '.vtx[4:7]', r=1)
            nearCluster = cmds.cluster(n=prefix + 'camera_nearFrustum_cluster')
            cmds.select(frustumGeo[0] + '.vtx[0:3]', r=1)
            farCluster = cmds.cluster(n=prefix + 'camera_farFrustum_cluster')

        #create near/far/camera locs
            cameraLoc = cmds.spaceLocator(p=(0, 0, 0), n=prefix + 'camera_loc')
            cmds.parent(cameraLoc[0], frustumMainGrp)
            nearLoc = cmds.spaceLocator(p=(0, 0, 0), n=prefix + 'camera_nearFrustum_loc')
            cmds.move(0, 0, -1)
            farLoc = cmds.spaceLocator(p=(0, 0, 0), n=prefix + 'camera_farFrustum_loc')
            cmds.move(0, 0, 1)

        #parent clusters under loc -- parent locs under camera loc
            cmds.parent(nearCluster[1], nearLoc[0])
            cmds.parent(farCluster[1], farLoc[0])
            cmds.parent(nearLoc[0], cameraLoc[0])
            cmds.parent(farLoc[0], cameraLoc[0]) 
        #constrain camera loc to camera
            cmds.parentConstraint(selCamXform, cameraLoc, weight=1)
        
        return frustumGeo[0]


def cameraFrustum_scale(cam_shape):
    #make sure the frustum geo exists
    prefix = 'frust_'
    frustumGrpName = prefix + 'camera_frustum_all_grp'
    if cmds.objExists(frustumGrpName)==1:
    #get loaded camera
        prefix = 'frust_'
        selCamXform = cmds.listRelatives(cam_shape[0], p=1)

    #get camera data
        verticalFieldOfView = cmds.camera(selCamXform, q=1, vfv=1)
        horizontalFieldOfView = cmds.camera(selCamXform, q=1, hfv=1)
        lensSqueezeRatio = cmds.camera(selCamXform, q=1, lsr=1)
        cameraScale = cmds.camera(selCamXform, q=1, cs=1)
        nearClipPlane = cmds.getAttr('{0}.nearClipPlane'format(cam_shape))
        farClipPlane = cmds.getAttr('{0}.farClipPlane'format(cam_shape))

    #convert degrees to radians if needed
        angleUnits = cmds.currentUnit(q=1, a=1)
        if angleUnits == 'deg':
            verticalFieldOfView = verticalFieldOfView * 0.0174532925
            horizontalFieldOfView = horizontalFieldOfView * 0.0174532925

    #get X/Y coordinates in 2d
        verticalAngle = math.tan(verticalFieldOfView *.5)
        horizontalAngle = math.tan(horizontalFieldOfView *.5)

    #apply camera lens squeeze
        horizontalFieldOfView = horizontalFieldOfView * lensSqueezeRatio;

    #apply camera scale 
        verticalAngle = verticalAngle * cameraScale;
        horizontalFieldOfView = horizontalFieldOfView * cameraScale;

    #set camera near and far locs
        nearClipPLaneOffset = 0
        cmds.setAttr('frust_camera_nearFrustum_loc.translateZ', -nearClipPlane+nearClipPLaneOffset)
        cmds.setAttr('frust_camera_farFrustum_loc.translateZ', -farClipPlane)

    #get maya linear working units
        linearUnits = cmds.currentUnit(q=1, l=1)
        factor = 1.0
        if 'mm' == linearUnits:
            factor = 0.1
        if 'm' == linearUnits:
            factor = 100
        if 'in' == linearUnits:
            factor = 2.54
        if 'ft' == linearUnits:
            factor = 30.48
        if 'yd' == linearUnits:
            factor = 91.44

    #get the near and far new scale
        nearScaleX = math.fabs(((nearClipPlane-nearClipPLaneOffset)*horizontalAngle)*factor)
        nearScaleY = math.fabs(((nearClipPlane-nearClipPLaneOffset)*verticalAngle)*factor)
        farScaleX = math.fabs((farClipPlane*horizontalAngle)*factor)
        farScaleY = math.fabs((farClipPlane*verticalAngle)*factor)

    #set scale
        scaleGain = 5
        cmds.setAttr('frust_camera_nearFrustum_loc.scaleX', nearScaleX+(scaleGain))
        cmds.setAttr('frust_camera_nearFrustum_loc.scaleY', nearScaleY+(scaleGain))
        cmds.setAttr('frust_camera_farFrustum_loc.scaleX', farScaleX+(scaleGain))
        cmds.setAttr('frust_camera_farFrustum_loc.scaleY', farScaleY+(scaleGain))

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


# get each object in frustum and facing camera at the same time
def getFacesInFrustum(container,obj):
    # select faces in container(frustum)
    allVtx = cmds.ls('{0}.vtx[:]'.format(obj),fl=True)
    allIn = []
    for vtx in allVtx:
      location = cmds.pointPosition(vtx,w=True)
      test = pyRayIntersect(container,location,(0,1,0))
      if(test):
          allIn.append(vtx)
    inner_faces = cmds.polyListComponentConversion(allIn,fv=True,tf=True)
    
    # select faces that facing the camera
    cmds.select(obj,r=True)
    cmds.selectMode(co=True)
    cmds.selectType(pf=True)
    cmds.setAttr('{0}.backfaceCulling'.format(obj[0]),2)
    view = OMU.M3dView.active3dView()
    OM.MGlobal.selectFromScreen(0, 0, view.portWidth(), view.portHeight(), OM.MGlobal.kReplaceList)
    facing_cam_faces = cmds.ls(sl=True,fl=True)
    
    # combine both selection
    all_faces = [x for x in inner_faces if x in facing_cam_faces]
    return all_faces

def getAllFacesInFrustum():
    start_frame = 1
    end_frame = 50
    by_frame = 5
    cur_frame = cmds.currentTime()
    
    sels = cmds.ls(sl=True,fl=True)
    cam_shape = cmds.ls(sels[-1],dag=True,type='shape')
    objs = sels[:-1]
    all_faces = []
    for frame in range(start_frame,end_frame+1,by_frame):
        set frame (frame)
        container = cameraFrustum_build(cam_shape)
        cameraFrustum_scale(cam_shape)
        for obj in objs:
            for face in getFacesInFrustum(container,obj):
                all_faces.append(face)
