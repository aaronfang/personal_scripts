#|############################################################################################################
#
# NAME: 
#     cameraFrustum
#
# AUTHOR:
#     Kiel Gnebba (ksg@kielgnebba.com)
#		
# VERSION: 
#     v. 1.0
#
# DESCRIPTION: 
#     This script will...
#         - allow you to select differents types of objects that are inside the camera frustum
#         - default is all visible for current frame
#         - uncheck "current frame only" to run the whole timeline
#
# INSTALLATION:
#     Copy the script into your scripts/ directory
#     If you're unsure where that is run this in the script editor:
#         mel    == internalVar -userScriptDir;
#         python == import maya.cmds as cmds; print cmds.internalVar(userScriptDir=True)
#
# USAGE:
#     To use just run: 
#         import maya.cmds as cmds
#         scriptName = 'cameraFrustum'
#         scriptsDir = cmds.internalVar(userScriptDir=True)
#         execfile(scriptsDir + scriptName + '.py')
#         cameraFrustum() 
#        
#     Or you can call the file directly from where ever you put it
#         execfile(C:/...where_ever.../cameraFrustum.py)
#         cameraFrustum()
#
# HISTORY:
#     03/21/2011 -- v. 1.0
#         - first release
#     
#|############################################################################################################

#import
import time
import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import math
import maya.mel as mel


#*************************************************************************************************************
#*start cameraFrustum_loadCamera()

def cameraFrustum_loadCamera():
    proc = 'cameraFrustum_loadCamera'
    printString = '\n\n////////////////////////////////////////////////////////////////////////////////////////////\n'
    printString += ('// ' + proc + ' details: \n//\n')

#-------------------------------------------------------------------------------------------------------------
#get selected camera
    selCamShape = cmds.ls(sl=1, dag=1, type='shape', long=1)

#make sure only 1 camera is selected
    if len(selCamShape)==0:
        cmds.warning('nothing selected...select a camera and load')
    elif len(selCamShape)>1:
        cmds.warning('more then one thing selected...select a camera and load')
    elif cmds.nodeType(selCamShape[0]) != 'camera':
        cmds.warning('selected object \"' + selCamShape[0] + '\" is not a camera...select a camera and load')
    else:
#remove any camera in list and load selected camera into ui
        camera = selCamShape[0]
        cmds.textScrollList('cameraFrustum_loadCameraTSL', e=1, ra=1)
        cmds.textScrollList('cameraFrustum_loadCameraTSL', e=1, a=[camera])
        cameraFrustum_refreshClip()

#-------------------------------------------------------------------------------------------------------------
#print
    printString += '////////////////////////////////////////////////////////////////////////////////////////////\n\n'
    #print printString
    #print ('COMPLETE -- check script editor for details...\n')

#*************************************************************************************************************
#*end cameraFrustum_loadCamera()

'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

#*************************************************************************************************************
#*start cameraFrustum_toggleClip()

def cameraFrustum_toggleClip():
    proc = 'cameraFrustum_toggleClip'
    printString = '\n\n////////////////////////////////////////////////////////////////////////////////////////////\n'
    printString += ('// ' + proc + ' details: \n//\n')

#-------------------------------------------------------------------------------------------------------------
#get loaded camera
    cameraLoaded = cmds.textScrollList('cameraFrustum_loadCameraTSL', q=1, ni=1)

#make sure a camera is loaded
    if cameraLoaded==0:
        cmds.warning('no camera loaded...select a camera and load')
    else:
    #determin if clipping plane is on or off
        selCamShape = cmds.textScrollList('cameraFrustum_loadCameraTSL', q=1, ai=1)
        clipDisplay = cmds.renderManip(selCamShape[0], q=1, cam=1)
        clipDisplayOn = 0
        if clipDisplay[3] == 0:
            clipDisplayOn = 1
    #toggle
        cmds.renderManip(selCamShape[0], e=1, cam=(clipDisplay[0], clipDisplay[1], clipDisplay[2], clipDisplayOn,  clipDisplay[4])) 

#-------------------------------------------------------------------------------------------------------------
#print
    printString += '////////////////////////////////////////////////////////////////////////////////////////////\n\n'
    #print printString
    #print ('COMPLETE -- check script editor for details...\n')

#*************************************************************************************************************
#*end cameraFrustum_toggleClip()

'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

#*************************************************************************************************************
#*start cameraFrustum_toggleFrustum()

def cameraFrustum_toggleFrustum():
    proc = 'cameraFrustum_toggleFrustum'
    printString = '\n\n////////////////////////////////////////////////////////////////////////////////////////////\n'
    printString += ('// ' + proc + ' details: \n//\n')

#-------------------------------------------------------------------------------------------------------------
#check if frustum exists and toggle on or off    
    prefix = 'frust_'
    frustumGrpName = prefix + 'camera_frustum_all_grp'
    if cmds.objExists(frustumGrpName)==1:
        deleteFrustStuff = cmds.ls('frust*')
        cmds.delete(deleteFrustStuff) 
    else:
        cameraFrustum_build()
        cameraFrustum_scale()

#-------------------------------------------------------------------------------------------------------------
#print
    printString += '////////////////////////////////////////////////////////////////////////////////////////////\n\n'
    #print printString
    #print ('COMPLETE -- check script editor for details...\n')

#*************************************************************************************************************
#*end cameraFrustum_toggleFrustum()

'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

#*************************************************************************************************************
#*start cameraFrustum_refreshClip()

def cameraFrustum_refreshClip():
    proc = 'cameraFrustum_refreshClip'
    printString = '\n\n////////////////////////////////////////////////////////////////////////////////////////////\n'
    printString += ('// ' + proc + ' details: \n//\n')

#-------------------------------------------------------------------------------------------------------------
#get loaded camera
    cameraLoaded = cmds.textScrollList('cameraFrustum_loadCameraTSL', q=1, ni=1)

#make sure a camera is loaded
    if cameraLoaded==0:
        cmds.warning('no camera loaded...select a camera and load')
    else:
    #get current clipping plane values
        selCamShape = cmds.textScrollList('cameraFrustum_loadCameraTSL', q=1, ai=1)
        selCamXform = cmds.listRelatives(selCamShape[0], p=1)
        nearClipPlane = cmds.camera(selCamXform, q=1, ncp=1)
        farClipPlane = cmds.camera(selCamXform, q=1, fcp=1)

    #update ui
        cmds.floatFieldGrp('cameraFrustum_nearFF', e=1, value1=nearClipPlane)
        cmds.floatFieldGrp('cameraFrustum_farFF', e=1, value1=farClipPlane)

#-------------------------------------------------------------------------------------------------------------
#print
    printString += '////////////////////////////////////////////////////////////////////////////////////////////\n\n'
    #print printString
    #print ('COMPLETE -- check script editor for details...\n')

#*************************************************************************************************************
#*end cameraFrustum_refreshClip()

'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

#*************************************************************************************************************
#*start cameraFrustum_selectAllDataType()

def cameraFrustum_selectAllDataType():
    proc = 'cameraFrustum_selectAllDataType'
    printString = '\n\n////////////////////////////////////////////////////////////////////////////////////////////\n'
    printString += ('// ' + proc + ' details: \n//\n')

#-------------------------------------------------------------------------------------------------------------
#select all data type check boxes
    chkBoxList = cmds.gridLayout('cameraFrustum_typeGrid', q=1, ca=1)
    eachChkBox = chkBoxList[0]
    for eachChkBox in chkBoxList:
        isSelected = cmds.checkBox(eachChkBox, q=1, value=1)
        if isSelected == 0:
            cmds.checkBox(eachChkBox, e=1, value=1)

#-------------------------------------------------------------------------------------------------------------
#print
    printString += '////////////////////////////////////////////////////////////////////////////////////////////\n\n'
    #print printString
    #print ('COMPLETE -- check script editor for details...\n')

#*************************************************************************************************************
#*end cameraFrustum_selectAllDataType()

'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

#*************************************************************************************************************
#*start cameraFrustum_deSelectAllDataType()

def cameraFrustum_deSelectAllDataType():
    proc = 'cameraFrustum_deSelectAllDataType'
    printString = '\n\n////////////////////////////////////////////////////////////////////////////////////////////\n'
    printString += ('// ' + proc + ' details: \n//\n')

#-------------------------------------------------------------------------------------------------------------
#select all data type check boxes
    chkBoxList = cmds.gridLayout('cameraFrustum_typeGrid', q=1, ca=1)
    eachChkBox = chkBoxList[0]
    for eachChkBox in chkBoxList:
        isSelected = cmds.checkBox(eachChkBox, q=1, value=1)
        if isSelected == 1:
            cmds.checkBox(eachChkBox, e=1, value=0)

#-------------------------------------------------------------------------------------------------------------
#print
    printString += '////////////////////////////////////////////////////////////////////////////////////////////\n\n'
    #print printString
    #print ('COMPLETE -- check script editor for details...\n')

#*************************************************************************************************************
#*end cameraFrustum_deSelectAllDataType()

'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

#*************************************************************************************************************
#*start cameraFrustum_build()

def cameraFrustum_build():
    procString = 'cameraFrustum_build'
    printString = '\n\n////////////////////////////////////////////////////////////////////////////////////////////\n'
    printString += ('// ' + procString + ' details: \n//\n')

#-------------------------------------------------------------------------------------------------------------
#get current selection
    selection = cmds.ls(sl=1)

#get loaded camera
    cameraLoaded = cmds.textScrollList('cameraFrustum_loadCameraTSL', q=1, ni=1)

#make sure a camera is loaded
    if cameraLoaded==0:
        cmds.error('no camera loaded...select a camera and load')
    else:
    #create frustum only if one doesnt already exist
        selCamShape = cmds.textScrollList('cameraFrustum_loadCameraTSL', q=1, ai=1)
        selCamXform = cmds.listRelatives(selCamShape[0], p=1)
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
            
#reselect original selection
    if len(selection) > 0:
        cmds.select(selection, r=1)
    
#-------------------------------------------------------------------------------------------------------------
#print
    printString += '////////////////////////////////////////////////////////////////////////////////////////////\n\n'
    #print printString
    #print ('COMPLETE -- check script editor for details...\n')

#*************************************************************************************************************
#*end cameraFrustum_build()

'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

#*************************************************************************************************************
#*start cameraFrustum_scale()

def cameraFrustum_scale():
    procString = 'cameraFrustum_scale'
    printString = '\n\n////////////////////////////////////////////////////////////////////////////////////////////\n'
    printString += ('// ' + procString + ' details: \n//\n')

#-------------------------------------------------------------------------------------------------------------
#make sure the frustum geo exists
    prefix = 'frust_'
    frustumGrpName = prefix + 'camera_frustum_all_grp'
    if cmds.objExists(frustumGrpName)==1:
    #get loaded camera
        prefix = 'frust_'
        selCamShape = cmds.textScrollList('cameraFrustum_loadCameraTSL', q=1, ai=1)
        selCamXform = cmds.listRelatives(selCamShape[0], p=1)

    #get camera data
        verticalFieldOfView = cmds.camera(selCamXform, q=1, vfv=1)
        horizontalFieldOfView = cmds.camera(selCamXform, q=1, hfv=1)
        lensSqueezeRatio = cmds.camera(selCamXform, q=1, lsr=1)
        cameraScale = cmds.camera(selCamXform, q=1, cs=1)
        nearClipPlane = cmds.floatFieldGrp('cameraFrustum_nearFF', q=1, value1=1)
        farClipPlane = cmds.floatFieldGrp('cameraFrustum_farFF', q=1, value1=1)

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
        scaleGain = cmds.floatFieldGrp('cameraFrustum_scaleGainFF', q=1, value1=1)
        cmds.setAttr('frust_camera_nearFrustum_loc.scaleX', nearScaleX+(scaleGain))
        cmds.setAttr('frust_camera_nearFrustum_loc.scaleY', nearScaleY+(scaleGain))
        cmds.setAttr('frust_camera_farFrustum_loc.scaleX', farScaleX+(scaleGain))
        cmds.setAttr('frust_camera_farFrustum_loc.scaleY', farScaleY+(scaleGain))

#-------------------------------------------------------------------------------------------------------------
#print
    printString += '////////////////////////////////////////////////////////////////////////////////////////////\n\n'
    #print printString
    #print ('COMPLETE -- check script editor for details...\n')

#*************************************************************************************************************
#*end cameraFrustum_scale()

'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

#*************************************************************************************************************
#*start cameraFrustum_check()

def cameraFrustum_check():
    procString = 'cameraFrustum_check'
    printString = '\n\n////////////////////////////////////////////////////////////////////////////////////////////\n'
    printString += ('// ' + procString + ' details: \n//\n')
    startTime = time.time()
    gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')
    isCancelled=0
    
#-------------------------------------------------------------------------------------------------------------
#get current panel
    curPanel = cmds.getPanel(withFocus=1)
    
#determine current show settings
    currentShowSettings=[]
    if curPanel[0:10] == 'modelPanel':
        currentShowSettings.append (cmds.modelEditor(curPanel, q=1, nurbsCurves=1))
        currentShowSettings.append (cmds.modelEditor(curPanel, q=1, nurbsSurfaces=1))
        currentShowSettings.append (cmds.modelEditor(curPanel, q=1, polymeshes=1))
        currentShowSettings.append (cmds.modelEditor(curPanel, q=1, subdivSurfaces=1))
        currentShowSettings.append (cmds.modelEditor(curPanel, q=1, planes=1))
        currentShowSettings.append (cmds.modelEditor(curPanel, q=1, lights=1))
        currentShowSettings.append (cmds.modelEditor(curPanel, q=1, cameras=1))
        currentShowSettings.append (cmds.modelEditor(curPanel, q=1, joints=1))
        currentShowSettings.append (cmds.modelEditor(curPanel, q=1, ikHandles=1))
        currentShowSettings.append (cmds.modelEditor(curPanel, q=1, deformers=1))
        currentShowSettings.append (cmds.modelEditor(curPanel, q=1, dynamics=1))
        currentShowSettings.append (cmds.modelEditor(curPanel, q=1, fluids=1))
        currentShowSettings.append (cmds.modelEditor(curPanel, q=1, hairSystems=1))
        currentShowSettings.append (cmds.modelEditor(curPanel, q=1, follicles=1))
        currentShowSettings.append (cmds.modelEditor(curPanel, q=1, nCloths=1))
        currentShowSettings.append (cmds.modelEditor(curPanel, q=1, nParticles=1))
        currentShowSettings.append (cmds.modelEditor(curPanel, q=1, nRigids=1))
        currentShowSettings.append (cmds.modelEditor(curPanel, q=1, dynamicConstraints=1))
        currentShowSettings.append (cmds.modelEditor(curPanel, q=1, locators=1))
        currentShowSettings.append (cmds.modelEditor(curPanel, q=1, dimensions=1))
        currentShowSettings.append (cmds.modelEditor(curPanel, q=1, pivots=1))
        currentShowSettings.append (cmds.modelEditor(curPanel, q=1, handles=1))
        currentShowSettings.append (cmds.modelEditor(curPanel, q=1, textures=1))
        currentShowSettings.append (cmds.modelEditor(curPanel, q=1, strokes=1))
        currentShowSettings.append (cmds.modelEditor(curPanel, q=1, manipulators=1))
    #set all to none
        cmds.modelEditor(curPanel, e=1, allObjects=0)

#current camera 
    selCamShape = cmds.textScrollList('cameraFrustum_loadCameraTSL', q=1, ai=1)
    selCamXform = cmds.listRelatives(selCamShape[0], p=1, fullPath=1)
    
#determin action
    actionInvert = cmds.checkBox('cameraFrustum_actionInvertCB', q=1, value=1)
    actionSelect = cmds.checkBox('cameraFrustum_actionSelectCB',  q=1, value=1)
    actionHide = cmds.checkBox('cameraFrustum_actionHideCB',  q=1, value=1)
    actionDelete = cmds.checkBox('cameraFrustum_actionDeleteCB',  q=1, value=1)
    actionLayer = cmds.checkBox('cameraFrustum_actionDisplayLayerCB',  q=1, value=1)
    actionKeep = cmds.checkBox('cameraFrustum_actionKeepCB',  q=1, value=1)

#determin limits
    limitEverything = cmds.checkBox('cameraFrustum_limitsEverythingCB', q=1, value=1)
    limitSelection = cmds.checkBox('cameraFrustum_limitsSelectionCB', q=1, value=1)
    limitVisible = cmds.checkBox('cameraFrustum_limitsVisibleCB', q=1, value=1)	
    limitRL = cmds.checkBox('cameraFrustum_limitsRLCB', q=1, value=1)
    limitGrp = cmds.checkBox('cameraFrustum_limitsInsideGrpCB', q=1, value=1)
    limitGrpName = cmds.textField('cameraFrustum_limitsInsideGrpTXT', q=1, text=1)
    limitWild = cmds.checkBox('cameraFrustum_limitsWildCardCB', q=1, value=1)
    limitWildName = cmds.textField('cameraFrustum_limitsWildCardTXT', q=1, text=1)

#determin type
    typeMesh = cmds.checkBox('cameraFrustum_typeMeshCB', q=1, value=1)
    typeLocators = cmds.checkBox('cameraFrustum_typeLocatorsCB', q=1, value=1)
    typeNurbs = cmds.checkBox('cameraFrustum_typeNurbsCB', q=1, value=1)
    typeLights = cmds.checkBox('cameraFrustum_typeLightsCB', q=1, value=1)
    typeCurves = cmds.checkBox('cameraFrustum_typeCurvesCB', q=1, value=1)
    typeDynamics = cmds.checkBox('cameraFrustum_typeDynamicsCB', q=1, value=1)
    typeJoints = cmds.checkBox('cameraFrustum_typeJointsCB', q=1, value=1)
    typeCameras = cmds.checkBox('cameraFrustum_typeCamerasCB', q=1, value=1)

#create all selection lists     
    allMesh = []
    allMesh[:] = []    
    allNurbs = []
    allNurbs[:] = []
    allCurves = []
    allCurves[:] = []
    allLocators = []
    allLocators[:] = []
    allLights = []
    allLights[:] = []
    allDynamics = []
    allDynamics[:] = []
    allJoints = [] 
    allJoints[:] = []
    allCameras = [] 
    allCameras[:] = []
    allSelection = []        
    allSelection[:] = []
    
#get select objects
    if limitSelection == 1:    
        allSelection = cmds.ls(sl=1, long=1)
        cmds.select(cl=1)
    elif limitVisible == 1:
        allSelection = cmds.ls(visible=1, transforms=1, long=1)
    elif limitRL == 1:
        currentRenderLayer = cmds.editRenderLayerGlobals(q=1, currentRenderLayer=1)
        allSelection = cmds.editRenderLayerMembers(currentRenderLayer, query=True, fullNames=1)
    elif limitGrp == 1:
        if cmds.objExists(limitGrpName)==1:
            allSelection = cmds.listRelatives(limitGrpName, allDescendents=1, fullPath=1)
        else:
            cmds.warning('no group named: ' + str(limitGrpName))
    elif limitWild == 1:
        selectString = 'catch(`select -r "' + limitWildName + '"`)'
        mel.eval(selectString)
        wildSelection = []
        wildSelection[:] = []
        wildSelection = cmds.ls(long=1, sl=1)
        cmds.select(cl=1)
        if len(wildSelection)>0:
            allSelection = wildSelection
        else:
            cmds.warning('nothing with this namespace: ' + str(limitGrpName))
    
#get all meshes 
    if typeMesh == 1:
        if limitEverything == 1:
            allMesh = cmds.ls(long=1, type='mesh')
        if limitSelection == 1 or limitVisible == 1 or limitRL == 1 or limitGrp == 1 or limitWild == 1:
            for eachSelection in allSelection:
                cmds.select(eachSelection, r=1)
                eachType = cmds.ls(sl=1, dag=1, type='shape', long=1)
                if len(eachType) > 0:
                    nodeType = cmds.nodeType(eachType[0])
                    if nodeType == 'mesh':
                        allMesh.append(eachType[0])
#get all nurbs
    if typeNurbs == 1:
        if limitEverything == 1:
            allNurbs = cmds.ls(long=1, type='nurbsSurface')
        if limitSelection == 1 or limitVisible == 1 or limitRL == 1 or limitGrp == 1 or limitWild == 1:
            for eachSelection in allSelection:
                cmds.select(eachSelection, r=1)
                eachType = cmds.ls(sl=1, dag=1, type='shape')
                if len(eachType) > 0:
                    nodeType = cmds.nodeType(eachType[0])
                    if nodeType == 'nurbsSurface':
                        allNurbs.append(eachType[0])
#get all curves
    if typeCurves == 1:
        if limitEverything == 1:
            allCurves = cmds.ls(long=1, type='nurbsCurve')
        if limitSelection == 1 or limitVisible == 1 or limitRL == 1 or limitGrp == 1 or limitWild == 1:
            for eachSelection in allSelection:
                cmds.select(eachSelection, r=1)
                eachType = cmds.ls(sl=1, dag=1, type='shape', long=1)
                if len(eachType) > 0:
                    nodeType = cmds.nodeType(eachType[0])
                    if nodeType == 'nurbsCurve':
                        allCurves.append(eachType[0])
#get all locators
    if typeLocators == 1:
        if limitEverything == 1:
            allLocators = cmds.ls(long=1, type='locator')
        if limitSelection == 1 or limitVisible == 1 or limitRL == 1 or limitGrp == 1 or limitWild == 1:
            for eachSelection in allSelection:
                cmds.select(eachSelection, r=1)
                eachType = cmds.ls(sl=1, dag=1, type='shape', long=1)
                if len(eachType) > 0:
                    nodeType = cmds.nodeType(eachType[0])
                    if nodeType == 'locator':
                        allLocators.append(eachType[0])
#get all joints
    if typeJoints == 1:
        if limitEverything == 1:
            allJoints = cmds.ls(long=1, type='joint')
        if limitSelection == 1 or limitVisible == 1 or limitRL == 1 or limitGrp == 1 or limitWild == 1:
            for eachSelection in allSelection:
                cmds.select(eachSelection, r=1)
                eachType = cmds.ls(sl=1)
                if len(eachType) > 0:
                    nodeType = cmds.nodeType(eachType[0])
                    if nodeType == 'joint':
                        allJoints.append(eachType[0])
                        
#get all cameras
    if typeCameras == 1:
        if limitEverything == 1:
            allCameras = cmds.ls(long=1, cameras=1)
        if limitSelection == 1 or limitVisible == 1 or limitRL == 1 or limitGrp == 1 or limitWild == 1:
            for eachSelection in allSelection:
                cmds.select(eachSelection, r=1)
                eachType = cmds.ls(sl=1, dag=1, type='shape', long=1)
                if len(eachType) > 0:
                    nodeType = cmds.nodeType(eachType[0])
                    if nodeType == 'camera':
                        allCameras.append(eachType[0])

#get all lights
    if typeLights == 1:
        if limitEverything == 1:
            allLights = cmds.ls(long=1, lights=1)
        if limitSelection == 1 or limitVisible == 1 or limitRL == 1 or limitGrp == 1 or limitWild == 1:
            for eachSelection in allSelection:
                cmds.select(eachSelection, r=1)
                eachType = cmds.ls(sl=1, dag=1, type='shape', long=1)
                if len(eachType) > 0:
                    nodeType = cmds.nodeType(eachType[0])
                    if nodeType == 'ambientLight' or nodeType == 'directionalLight' or nodeType == 'pointLight' or nodeType == 'spotLight' or nodeType == 'areaLight' or nodeType == 'volumeLight':
                        allLights.append(eachType[0])
                        
#get all dynamics
    if typeDynamics == 1:
        if limitEverything == 1:
            allEmitters = cmds.ls(long=1, type='pointEmitter')
            allnParticle = cmds.ls(long=1, type='nParticle')
            allParticles = cmds.ls(long=1, type='particle')
            allAirField = cmds.ls(long=1, type='airField')
            allDragField = cmds.ls(long=1, type='dragField')
            allGravityField = cmds.ls(long=1, type='gravityField')
            allNewtonField = cmds.ls(long=1, type='newtonField')
            allRadialField = cmds.ls(long=1, type='radialField')  
            allTurbulenceField = cmds.ls(long=1, type='turbulenceField')
            allUniformField = cmds.ls(long=1, type='uniformField')
            allVortexField = cmds.ls(long=1, type='vortexField')
            allVolumeAxisField = cmds.ls(long=1, type='volumeAxisField')
            allFluids = cmds.ls(long=1, type='fluidShape')
            allDynamics = allEmitters + allnParticle + allParticles + allAirField + allDragField + allGravityField + allNewtonField + allRadialField + allTurbulenceField + allUniformField + allVortexField + allVolumeAxisField + allFluids
        if limitSelection == 1 or limitVisible == 1 or limitRL == 1 or limitGrp == 1 or limitWild == 1:
            for eachSelection in allSelection:
                cmds.select(eachSelection, r=1)
                eachType = cmds.ls(sl=1, dag=1, type='shape', long=1)
                if len(eachType) > 0:
                    nodeType = cmds.nodeType(eachType[0])
                    if nodeType == 'nParticle' or nodeType == 'particle' or nodeType == 'fluidShape':
                        allDynamics.append(eachType[0]) 
                else:
                    nodeType = cmds.nodeType(eachSelection)
                    if nodeType == 'pointEmitter' or nodeType == 'airField' or nodeType == 'dragField' or nodeType == 'gravityField' or nodeType == 'newtonField' or nodeType == 'radialField' or nodeType == 'turbulenceField' or nodeType == 'uniformField' or nodeType == 'vortexField' or nodeType == 'volumeAxisField':
                        allDynamics.append(eachSelection) 

#list for object inside frustum
    insideFrustum=[]
    insideFrustum[:] = []
    insideFrustumAll=[]
    insideFrustumAll[:] = []    
    allTypes = []
    allTypes[:] = []
    allTypes += allMesh + allNurbs + allCurves + allLocators + allJoints + allCameras + allLights + allDynamics
    allTypes = list(set(allTypes))
    allTypesStart = []
    allTypesStart[:] = []
    allTypesStart = allTypes
            
#get start, end and increment frame
    startFrame = cmds.intField('cameraFrustum_startIF', q=1, value=1)
    endFrame = cmds.intField('cameraFrustum_endIF', q=1, value=1)
    frameIncrement = cmds.intField('cameraFrustum_keyIF', q=1, value=1)
    currentFrame = cmds.currentTime(q=1)
    currentFrameOnly = cmds.checkBox('cameraFrustum_currentFrameCB', q=1, value=1)
    if currentFrameOnly == 1:
        startFrame = currentFrame
        endFrame = currentFrame
        frameIncrement = 1
        
#progress bar
    bakingText = 'Frustum Checking......(Press ESC To Cancel)'
    progressAmount = int(endFrame-startFrame)
    if currentFrameOnly == 1:
        progressAmount=1
    cmds.progressBar('cameraFrustum_progBar', e=1, maxValue=progressAmount)
    cmds.text('cameraFrustum_cancelTxt', e=1, label=bakingText) 
    cmds.progressBar('cameraFrustum_progBar', e=1, progress=0)
    cmds.progressBar(gMainProgressBar, edit=1, beginProgress=1, isInterruptable=1, status='Frustum Checking......', maxValue=progressAmount)
    
    if len(allTypes)>0:
        t = startFrame
        while t <= endFrame:
            cmds.currentTime(t, e=1)
            #for each in allTypes:
            e=0
            while e < len(allTypes):
                each = allTypes[e]
                #parent = cmds.listRelatives(each, p=1, f=1)
                #eachObject = str(parent[0])        
                objParent = cmds.listRelatives(each, p=1, f=1)
                parent=[]
                parent.append(objParent) 
                eachObject=''
                newParent = str(parent[0])        
                if newParent=='None':
                    eachObject = str(each)
                else:
                    eachObject = str(objParent[0])
                center = cmds.xform(eachObject ,q=1, ws=1, t=1)
                selBoundingBox = cmds.xform(eachObject ,q=1, ws=1, boundingBox=1)
                bBox_0 = center[0:3]
                bBox_1 = selBoundingBox[0:3]
                bBox_2 = [selBoundingBox[3]-selBoundingBox[0]+selBoundingBox[0], selBoundingBox[1], selBoundingBox[2]]
                bBox_3 = [selBoundingBox[0], (selBoundingBox[4]-selBoundingBox[1])+selBoundingBox[1], selBoundingBox[2]]
                bBox_4 = [(selBoundingBox[3]-selBoundingBox[0])+selBoundingBox[0], (selBoundingBox[4]-selBoundingBox[1])+selBoundingBox[1], selBoundingBox[2]]
                bBox_5 = [selBoundingBox[0], selBoundingBox[1], (selBoundingBox[5]-selBoundingBox[2])+selBoundingBox[2]]
                bBox_6 = [(selBoundingBox[3]-selBoundingBox[0])+selBoundingBox[0], selBoundingBox[1], (selBoundingBox[5]-selBoundingBox[2])+selBoundingBox[2]]
                bBox_7 = [selBoundingBox[0], (selBoundingBox[4]-selBoundingBox[1])+selBoundingBox[1], (selBoundingBox[5]-selBoundingBox[2])+selBoundingBox[2]]
                bBox_8 = [(selBoundingBox[3]-selBoundingBox[0])+selBoundingBox[0], (selBoundingBox[4]-selBoundingBox[1])+selBoundingBox[1], (selBoundingBox[5]-selBoundingBox[2])+selBoundingBox[2]]

                allBboxPoints = [
                bBox_0[0], bBox_0[1], bBox_0[2],
                bBox_1[0], bBox_1[1], bBox_1[2],
                bBox_2[0], bBox_2[1], bBox_2[2],
                bBox_3[0], bBox_3[1], bBox_3[2],
                bBox_4[0], bBox_4[1], bBox_4[2],
                bBox_5[0], bBox_5[1], bBox_5[2],
                bBox_6[0], bBox_6[1], bBox_6[2],
                bBox_7[0], bBox_7[1], bBox_7[2],
                bBox_8[0], bBox_8[1], bBox_8[2]]

                count = 0
                i=0
                while i < 27:
                    allBboxPointsVec = [allBboxPoints[i], allBboxPoints[i+1], allBboxPoints[i+2]]
                    cmds.setAttr ('frust_npomNode.inPositionX', allBboxPointsVec[0])
                    cmds.setAttr ('frust_npomNode.inPositionY', allBboxPointsVec[1])
                    cmds.setAttr ('frust_npomNode.inPositionZ', allBboxPointsVec[2])
                    closestPostionX = cmds.getAttr('frust_npomNode.positionX')
                    closestPostionY = cmds.getAttr('frust_npomNode.positionY')
                    closestPostionZ = cmds.getAttr('frust_npomNode.positionZ')

                # Create two MVectors
                    vectorA = OpenMaya.MVector(allBboxPointsVec[0], allBboxPointsVec[1], allBboxPointsVec[2])
                    vectorB = OpenMaya.MVector(closestPostionX, closestPostionY, closestPostionZ)
                    vectorC = (vectorA - vectorB)
                    vectorC.normalize()
                    position = [vectorC.x, vectorC.y, vectorC.z]
                    
                    norX = cmds.getAttr('frust_npomNode.normalX')
                    norY = cmds.getAttr('frust_npomNode.normalY')
                    norZ = cmds.getAttr('frust_npomNode.normalZ')
                    vectorD = OpenMaya.MVector(norX, norY, norZ)
                    vectorD.normalize()
                    normal = [vectorD.x, vectorD.y, vectorD.z]
                    
                    dotProd = (normal[0]*position[0]) + (normal[1]*position[1]) + (normal[2]*position[2])
                    #if actionInvert==0:
                    if dotProd >= 0:
                        count+=1
                        i=27
                    #else:
                        #if dotProd <= 0:
                            #count+=1
                            #i=27                
                    i+=3

                if count>0:
                    insideFrustum.append(each)
                    allTypes.remove(each)
                    e-=1
                e+=1
                
        #progress bar update or cancel
            if cmds.progressBar(gMainProgressBar, q=1, isCancelled=1):
                isCancelled=1
                cmds.progressBar('cameraFrustum_progBar', e=1, progress=0)
                cmds.text('cameraFrustum_cancelTxt', e=1, label='')          
                break

            cmds.progressBar('cameraFrustum_progBar', e=1, step=1)
            cmds.progressBar(gMainProgressBar, edit=1, step=1)      
            t+=frameIncrement
                  
#invert frustum 
    if actionInvert==0: 
        insideFrustumAll = insideFrustum
    else:
        insideFrustumAll = allTypesStart
        for each in insideFrustum:
            if each in allTypesStart:
                insideFrustumAll.remove(each)
                
#remove camera if in list
    if selCamShape[0] in insideFrustumAll:
        insideFrustumAll.remove(str(selCamShape[0]))
    if selCamXform[0] in insideFrustumAll:
        insideFrustumAll.remove(str(selCamXform[0]))
        
#action
    if actionSelect == 1:
        if len(insideFrustumAll)>0:
            cmds.select(insideFrustumAll, r=1)
        else:
            cmds.select(cl=1)
    
#delete all frust* stuff
    if actionKeep == 0:
        deleteFrustStuff = cmds.ls('frust*')
        cmds.delete(deleteFrustStuff) 
    
#return show selection
    if curPanel[0:10] == 'modelPanel':
        cmds.modelEditor(curPanel, e=1, nurbsCurves=currentShowSettings[0])
        cmds.modelEditor(curPanel, e=1, nurbsSurfaces=currentShowSettings[1])
        cmds.modelEditor(curPanel, e=1, polymeshes=currentShowSettings[2])
        cmds.modelEditor(curPanel, e=1, subdivSurfaces=currentShowSettings[3])
        cmds.modelEditor(curPanel, e=1, planes=currentShowSettings[4])
        cmds.modelEditor(curPanel, e=1, lights=currentShowSettings[5])
        cmds.modelEditor(curPanel, e=1, cameras=currentShowSettings[6])
        cmds.modelEditor(curPanel, e=1, joints=currentShowSettings[7])
        cmds.modelEditor(curPanel, e=1, ikHandles=currentShowSettings[8])
        cmds.modelEditor(curPanel, e=1, deformers=currentShowSettings[9])
        cmds.modelEditor(curPanel, e=1, dynamics=currentShowSettings[10])
        cmds.modelEditor(curPanel, e=1, fluids=currentShowSettings[11])
        cmds.modelEditor(curPanel, e=1, hairSystems=currentShowSettings[12])
        cmds.modelEditor(curPanel, e=1, follicles=currentShowSettings[13])
        cmds.modelEditor(curPanel, e=1, nCloths=currentShowSettings[14])
        cmds.modelEditor(curPanel, e=1, nParticles=currentShowSettings[15])
        cmds.modelEditor(curPanel, e=1, nRigids=currentShowSettings[16])
        cmds.modelEditor(curPanel, e=1, dynamicConstraints=currentShowSettings[17])
        cmds.modelEditor(curPanel, e=1, locators=currentShowSettings[18])
        cmds.modelEditor(curPanel, e=1, dimensions=currentShowSettings[19])
        cmds.modelEditor(curPanel, e=1, pivots=currentShowSettings[20])
        cmds.modelEditor(curPanel, e=1, handles=currentShowSettings[21])
        cmds.modelEditor(curPanel, e=1, textures=currentShowSettings[22])
        cmds.modelEditor(curPanel, e=1, strokes=currentShowSettings[23])
        cmds.modelEditor(curPanel, e=1, manipulators=currentShowSettings[24])
         
#timer
    endTime = time.time()
    totalTime =  (endTime - startTime)
    timeStr = ' seconds'
    if totalTime > 60:
        totalTime /= 60
        timeStr = ' minutes'

    if isCancelled == 0:    
        cmds.text('cameraFrustum_cancelTxt', e=1, label='Total Time: ' + str(totalTime) + timeStr)
    else: 
        cmds.text('cameraFrustum_cancelTxt', e=1, label='Cancelled -- Total Time: ' + str(totalTime) + timeStr)  

#progress bar end
    cmds.progressBar('cameraFrustum_progBar', e=1, progress=0)
    cmds.progressBar(gMainProgressBar, edit=1, endProgress=1)        

#-------------------------------------------------------------------------------------------------------------
#print
    #endTime = time.time()
    #totalTime =  endTime - startTime
    #printString += '// total time: ' + str(totalTime) + ' seconds\n'
    #printString += '////////////////////////////////////////////////////////////////////////////////////////////\n\n'
    #print printString
    #print ('COMPLETE -- check script editor for details...\n')

#*************************************************************************************************************
#*end cameraFrustum_check()

'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

#*************************************************************************************************************
#*start cameraFrustum()

def cameraFrustum():
    procString = 'cameraFrustum'
    printString = '\n\n////////////////////////////////////////////////////////////////////////////////////////////\n'
    printString += ('// ' + procString + ' details: \n//\n')

#-------------------------------------------------------------------------------------------------------------
#window creation
    if cmds.window('cameraFrustum_win', exists=1)==1:
        cmds.deleteUI('cameraFrustum_win')

    cmds.window('cameraFrustum_win', title="Camera Frustum Checking", resizeToFitChildren=1, maximizeButton=0, sizeable=1)

    cmds.formLayout('cameraFrustum_mainForm')     
    cmds.columnLayout('cameraFrustum_mainCol', adj=1, p='cameraFrustum_mainForm')
    cmds.text('cameraFrustum_cancelTxt', font='tinyBoldLabelFont', label='', align='center', w=60, p='cameraFrustum_mainForm')
    cmds.progressBar('cameraFrustum_progBar', maxValue=100, h=10, p='cameraFrustum_mainForm')
    cmds.button('cameraFrustum_executeButton', l='Build List', c='cameraFrustum_refreshClip(); cameraFrustum_build(); cameraFrustum_scale(); cameraFrustum_check()', h=10, p='cameraFrustum_mainForm') 

#load camera frameLayout     
    cmds.frameLayout('cameraFrustum_loadCameraFrame', l='Load Camera', marginHeight=5, collapsable=1, collapse=0, borderStyle='etchedIn', p='cameraFrustum_mainCol')
    cmds.formLayout('cameraFrustum_loadCameraForm', p='cameraFrustum_loadCameraFrame')
    cmds.textScrollList('cameraFrustum_loadCameraTSL', numberOfRows=1, annotation='double-click to select camera', doubleClickCommand='selCam = cmds.textScrollList(\'cameraFrustum_loadCameraTSL\', q=1, selectItem=1); cmds.select(selCam, r=1)', p='cameraFrustum_loadCameraForm')
    cmds.button('cameraFrustum_loadCameraButton', l='load', w=80, h=30, c='cameraFrustum_loadCamera()', p='cameraFrustum_loadCameraForm')
    
    cmds.formLayout('cameraFrustum_loadCameraForm',  e=1, 
    attachForm=[
    ('cameraFrustum_loadCameraButton', 'top', 5),
    ('cameraFrustum_loadCameraButton', 'left', 40),
    ('cameraFrustum_loadCameraButton', 'bottom', 5),
    ('cameraFrustum_loadCameraTSL', 'top', 5),
    ('cameraFrustum_loadCameraTSL', 'bottom', 5),
    ('cameraFrustum_loadCameraTSL', 'right', 40)
    ],
    attachControl=[                  
    ('cameraFrustum_loadCameraTSL', 'left', 40, 'cameraFrustum_loadCameraButton')
    ])
    
#build frustum frameLayout 
    cmds.frameLayout('cameraFrustum_buildFrustumFrame', l='Build Camera Frustum', marginHeight=5, collapsable=1, collapse=0, borderStyle='etchedIn', p='cameraFrustum_mainCol')
    cmds.formLayout('cameraFrustum_buildFrustumForm', p='cameraFrustum_buildFrustumFrame')
    cmds.button('cameraFrustum_refreshButton', l='refresh', w=45, h=35, c='cameraFrustum_refreshClip()', p='cameraFrustum_buildFrustumForm')
    cmds.floatFieldGrp('cameraFrustum_nearFF', el='  Near Clip Plane', value1=0, p='cameraFrustum_buildFrustumForm')
    cmds.floatFieldGrp('cameraFrustum_farFF', el='  Far Clip Plane', value1=1000, p='cameraFrustum_buildFrustumForm')
    cmds.floatFieldGrp('cameraFrustum_scaleGainFF', el='  Frustum Scale Gain', precision=3, value1=5, changeCommand='cameraFrustum_refreshClip();cameraFrustum_scale()', p='cameraFrustum_buildFrustumForm')
    cmds.button('cameraFrustum_toggleClipButton', l='clipping planes', w=90, h=20, c='cameraFrustum_toggleClip()', p='cameraFrustum_buildFrustumForm')
    cmds.button('cameraFrustum_buildFrustumButton', l='build frustum', w=80, h=20, c='cameraFrustum_toggleFrustum()', p='cameraFrustum_buildFrustumForm')
    
    cmds.formLayout('cameraFrustum_buildFrustumForm',  e=1, 
    attachForm=[
    ('cameraFrustum_refreshButton', 'top', 10),
    ('cameraFrustum_refreshButton', 'left', 25),
    ('cameraFrustum_nearFF', 'top', 4),
    ('cameraFrustum_nearFF', 'right', 20),
    ('cameraFrustum_nearFF', 'left', 92),
    ('cameraFrustum_farFF', 'left', 92),
    ('cameraFrustum_scaleGainFF', 'top', 4),
    ('cameraFrustum_scaleGainFF', 'left', 290),
    ('cameraFrustum_toggleClipButton', 'left', 290)
    ],
    attachControl=[                  
    ('cameraFrustum_farFF', 'top', 5, 'cameraFrustum_nearFF'),
    ('cameraFrustum_toggleClipButton', 'top', 4, 'cameraFrustum_scaleGainFF'),
    ('cameraFrustum_buildFrustumButton', 'top', 4, 'cameraFrustum_scaleGainFF'),
    ('cameraFrustum_buildFrustumButton', 'left', 10, 'cameraFrustum_toggleClipButton')
    ])

#frameRange frameLayout 
    cmds.frameLayout('cameraFrustum_frameRangeFrame', l='Frame Range Options', marginHeight=5, collapsable=1, collapse=0, borderStyle='etchedIn', p='cameraFrustum_mainCol')
    cmds.formLayout('cameraFrustum_frameRangeForm', p='cameraFrustum_frameRangeFrame')
    cmds.button('cameraFrustum_timeButton', l='time', w=35, h=35, c='cmds.intField(\'cameraFrustum_startIF\', e=1, value=cmds.playbackOptions(q=1, min=1));cmds.intField(\'cameraFrustum_endIF\', e=1, value=cmds.playbackOptions(q=1, max=1))', p='cameraFrustum_frameRangeForm')
    cmds.text('cameraFrustum_startFrameTxt', l='Start Frame', w=60, p='cameraFrustum_frameRangeForm')
    cmds.text('cameraFrustum_endFrameTxt', l='End Frame', w=60, p='cameraFrustum_frameRangeForm')
    cmds.intField('cameraFrustum_startIF', value=cmds.playbackOptions(q=1, min=1), editable=1, w=60, p='cameraFrustum_frameRangeForm')
    cmds.intField('cameraFrustum_endIF', value=cmds.playbackOptions(q=1, max=1), editable=1, w=60, p='cameraFrustum_frameRangeForm')
    cmds.checkBox('cameraFrustum_currentFrameCB', l='Current Frame Only', value=1, align='left', p='cameraFrustum_frameRangeForm')
    cmds.text('cameraFrustum_keyFrameTxt', l='Check Every', w=60, p='cameraFrustum_frameRangeForm')
    cmds.intField('cameraFrustum_keyIF', value=1, editable=1, minValue=1, w=60, p='cameraFrustum_frameRangeForm')

    cmds.formLayout('cameraFrustum_frameRangeForm',  e=1,
    attachForm=[
    ('cameraFrustum_timeButton', 'top', 8),
    ('cameraFrustum_timeButton', 'left', 45),
    ('cameraFrustum_startFrameTxt', 'top', 5),
    ('cameraFrustum_startIF', 'top', 2),
    ('cameraFrustum_currentFrameCB', 'top', 4)
    ],
    attachControl=[
    ('cameraFrustum_startFrameTxt', 'left', 30, 'cameraFrustum_timeButton'),
    ('cameraFrustum_endFrameTxt', 'top', 10, 'cameraFrustum_startFrameTxt'),
    ('cameraFrustum_endFrameTxt', 'left', 30, 'cameraFrustum_timeButton'),
    ('cameraFrustum_startIF', 'left', 5, 'cameraFrustum_startFrameTxt'),
    ('cameraFrustum_endIF', 'top', 4, 'cameraFrustum_startIF'),
    ('cameraFrustum_endIF', 'left', 5, 'cameraFrustum_endFrameTxt'),
    ('cameraFrustum_currentFrameCB', 'left', 56, 'cameraFrustum_startIF'),
    ('cameraFrustum_keyFrameTxt', 'left', 75, 'cameraFrustum_endIF'),
    ('cameraFrustum_keyFrameTxt', 'top', 9, 'cameraFrustum_currentFrameCB'),
    ('cameraFrustum_keyIF', 'top', 5, 'cameraFrustum_currentFrameCB'),
    ('cameraFrustum_keyIF', 'left', 5, 'cameraFrustum_keyFrameTxt')
    ])
    
#return data frameLayout 
    cmds.frameLayout('cameraFrustum_returnDataFrame', l='Return Data', marginHeight=5, collapsable=1, collapse=0, borderStyle='etchedIn', p='cameraFrustum_mainCol')
    cmds.formLayout('cameraFrustum_returnDataForm', p='cameraFrustum_returnDataFrame')
    cmds.columnLayout('cameraFrustum_actionCol', adj=1, p='cameraFrustum_returnDataForm')
    cmds.columnLayout('cameraFrustum_typeCol', adj=1, p='cameraFrustum_returnDataForm')

#data type frameLayout 
    cmds.frameLayout('cameraFrustum_typeFrame', l='Data Type', ec='cmds.frameLayout(\'cameraFrustum_componentFrame\', e=1, collapse=1)', marginHeight=5, collapsable=1, collapse=0, borderStyle='etchedIn', p='cameraFrustum_typeCol')
    cmds.formLayout('cameraFrustum_typeForm', p='cameraFrustum_typeFrame')
    cmds.button('cameraFrustum_typeAllButton', l='All', w=60, h=20, c='cameraFrustum_selectAllDataType()', p='cameraFrustum_typeForm')
    cmds.button('cameraFrustum_typeNoneButton', l='None', w=60, h=20, c='cameraFrustum_deSelectAllDataType()', p='cameraFrustum_typeForm')
    cmds.gridLayout('cameraFrustum_typeGrid', numberOfColumns=2, cellWidthHeight=(105, 20), p='cameraFrustum_typeForm')
    cmds.checkBox('cameraFrustum_typeMeshCB', l='Mesh', value=1, align='left', p='cameraFrustum_typeGrid')
    cmds.checkBox('cameraFrustum_typeJointsCB', l='Joints', value=1, align='left', p='cameraFrustum_typeGrid')
    cmds.checkBox('cameraFrustum_typeNurbsCB', l='Nurbs', value=1, align='left', p='cameraFrustum_typeGrid')
    cmds.checkBox('cameraFrustum_typeLightsCB', l='Lights', value=1, align='left', p='cameraFrustum_typeGrid')
    cmds.checkBox('cameraFrustum_typeCurvesCB', l='Curves', value=1, align='left', p='cameraFrustum_typeGrid')
    cmds.checkBox('cameraFrustum_typeDynamicsCB', l='Dynamics', value=1, align='left', p='cameraFrustum_typeGrid')
    cmds.checkBox('cameraFrustum_typeLocatorsCB', l='Locators', value=1, align='left', p='cameraFrustum_typeGrid')
    cmds.checkBox('cameraFrustum_typeCamerasCB', l='Cameras', value=1, align='left', p='cameraFrustum_typeGrid')
    
    cmds.formLayout('cameraFrustum_typeForm', e=1, 
    attachForm=[
    ('cameraFrustum_typeAllButton', 'left', 85),
    ('cameraFrustum_typeAllButton', 'top', 5),
    ('cameraFrustum_typeNoneButton', 'top', 5),
    ('cameraFrustum_typeGrid', 'left', 65),
    ('cameraFrustum_typeGrid', 'right', 0),
    ('cameraFrustum_typeGrid', 'bottom', 5)
    ],
    attachControl=[
    ('cameraFrustum_typeNoneButton', 'left', 10, 'cameraFrustum_typeAllButton'),
    ('cameraFrustum_typeGrid', 'top', 10, 'cameraFrustum_typeAllButton')
    ])
    
#component frameLayout 
    cmds.frameLayout('cameraFrustum_componentFrame', l='Component Type', ec='cmds.frameLayout(\'cameraFrustum_typeFrame\', e=1, collapse=1)', marginHeight=5, collapsable=1, collapse=1, borderStyle='etchedIn', p='cameraFrustum_typeCol')
    cmds.formLayout('cameraFrustum_componentForm', p='cameraFrustum_componentFrame')
    cmds.gridLayout('cameraFrustum_componentGrid', numberOfColumns=2, cellWidthHeight=(105, 20), p='cameraFrustum_componentForm')
    cmds.checkBox('cameraFrustum_typeVertexCB', l='Vertex', value=0, align='left', p='cameraFrustum_componentGrid')
    cmds.checkBox('cameraFrustum_typeEdgeCB', l='Edge', value=0, align='left', p='cameraFrustum_componentGrid')
    cmds.checkBox('cameraFrustum_typeFaceCB', l='Face', value=0, align='left', p='cameraFrustum_componentGrid')
    
    cmds.formLayout('cameraFrustum_componentForm', e=1, 
    attachForm=[
    ('cameraFrustum_componentGrid', 'left', 65),
    ('cameraFrustum_componentGrid', 'right', 0),
    ('cameraFrustum_componentGrid', 'top', 5),
    ('cameraFrustum_componentGrid', 'bottom', 5)
    ])    
    
#action frameLayout 
    cmds.frameLayout('cameraFrustum_actionFrame', l='Action', marginHeight=5, collapsable=1, collapse=0, borderStyle='etchedIn', p='cameraFrustum_actionCol')
    cmds.formLayout('cameraFrustum_actionForm', p='cameraFrustum_actionFrame')
    cmds.gridLayout('cameraFrustum_actionGrid', numberOfColumns=1, cellWidthHeight=(110, 20), p='cameraFrustum_actionForm')
    cmds.checkBox('cameraFrustum_actionInvertCB', l='Invert Frustum', value=0, align='left', p='cameraFrustum_actionGrid')
    cmds.checkBox('cameraFrustum_actionSelectCB', l='Select', value=1, align='left', p='cameraFrustum_actionGrid')
    cmds.checkBox('cameraFrustum_actionHideCB', l='Hide', enable=0, value=0, align='left', p='cameraFrustum_actionGrid')
    cmds.checkBox('cameraFrustum_actionDeleteCB', l='Delete', enable=0, value=0, align='left', p='cameraFrustum_actionGrid')
    cmds.checkBox('cameraFrustum_actionDisplayLayerCB', l='Display Layer', enable=0, value=0, align='left', p='cameraFrustum_actionGrid')
    cmds.checkBox('cameraFrustum_actionKeepCB', l='Keep Frustum Geo', value=0, align='left', p='cameraFrustum_actionGrid')
    
    cmds.formLayout('cameraFrustum_actionForm', e=1, 
    attachForm=[
    ('cameraFrustum_actionGrid', 'left', 15),
    ('cameraFrustum_actionGrid', 'right', 0),
    ('cameraFrustum_actionGrid', 'top', 5),
    ('cameraFrustum_actionGrid', 'bottom', 5)
    ])
    
#limits frameLayout 
    cmds.frameLayout('cameraFrustum_limitsFrame', l='Limits', marginHeight=5, collapsable=1, collapse=0, borderStyle='etchedIn', p='cameraFrustum_actionCol')
    cmds.formLayout('cameraFrustum_limitsForm', p='cameraFrustum_limitsFrame')
    cmds.gridLayout('cameraFrustum_limitsGrid', numberOfColumns=1, cellWidthHeight=(165, 20), p='cameraFrustum_limitsForm')
    cmds.checkBox('cameraFrustum_limitsEverythingCB', l='Everything', value=0, align='left', p='cameraFrustum_limitsGrid')
    cmds.checkBox('cameraFrustum_limitsSelectionCB', l='Selection', value=0, align='left', p='cameraFrustum_limitsGrid')
    cmds.checkBox('cameraFrustum_limitsVisibleCB', l='Visible', value=1, align='left', p='cameraFrustum_limitsGrid')	
    cmds.checkBox('cameraFrustum_limitsRLCB', l='Current Render Layer', value=0, align='left', p='cameraFrustum_limitsGrid')
    cmds.checkBox('cameraFrustum_limitsInsideGrpCB', l='Inside Group', value=0, align='left', p='cameraFrustum_limitsGrid')
    cmds.textField('cameraFrustum_limitsInsideGrpTXT', text='name of group')
    cmds.checkBox('cameraFrustum_limitsWildCardCB', l='*Wild Card*', value=0, align='left', p='cameraFrustum_limitsGrid')
    cmds.textField('cameraFrustum_limitsWildCardTXT', text='e.g. --  *name,  *:name')

    cmds.formLayout('cameraFrustum_limitsForm', e=1, 
    attachForm=[
    ('cameraFrustum_limitsGrid', 'left', 15),
    ('cameraFrustum_limitsGrid', 'right', 0),
    ('cameraFrustum_limitsGrid', 'top', 5),
    ('cameraFrustum_limitsGrid', 'bottom', 5)
    ])    
    
    #edit return data form
    cmds.formLayout('cameraFrustum_returnDataForm', e=1, 
    attachForm=[
    ('cameraFrustum_typeCol', 'top', 0),
    ('cameraFrustum_typeCol', 'right', 0),
    ('cameraFrustum_typeCol', 'bottom', 0),
    ('cameraFrustum_actionCol', 'top', 0),
    ('cameraFrustum_actionCol', 'left', 0),
    ('cameraFrustum_actionCol', 'bottom', 0)
    ],
    attachPosition=[
    ('cameraFrustum_typeCol', 'left', 0, 40),
    ('cameraFrustum_actionCol', 'right', 0, 40)
    ])

#edit mainForm
    cmds.formLayout('cameraFrustum_mainForm', e=1, 
    attachForm=[
    ('cameraFrustum_mainCol', 'top', 0),
    ('cameraFrustum_mainCol', 'left', 0),
    ('cameraFrustum_mainCol', 'right', 0),
    ('cameraFrustum_mainCol', 'bottom', 80),
    ('cameraFrustum_cancelTxt', 'left', 5),
    ('cameraFrustum_cancelTxt', 'right', 5),
    ('cameraFrustum_cancelTxt', 'bottom', 60),    
    ('cameraFrustum_progBar', 'left', 5),
    ('cameraFrustum_progBar', 'right', 5),
    ('cameraFrustum_progBar', 'bottom', 40),
    ('cameraFrustum_executeButton', 'left', 5),
    ('cameraFrustum_executeButton', 'right', 5),
    ('cameraFrustum_executeButton', 'bottom', 2)
    ],
    attachControl=[                  
    ('cameraFrustum_cancelTxt', 'top', 5, 'cameraFrustum_mainCol'),
    ('cameraFrustum_progBar', 'top', 5, 'cameraFrustum_cancelTxt'),
    ('cameraFrustum_executeButton', 'top', 5, 'cameraFrustum_progBar')
    ])  

#show and resize window        
    cmds.showWindow('cameraFrustum_win')  
    cmds.window('cameraFrustum_win', e=1, wh=[510,715]) 
    
#run some def's
    cameraFrustum_loadCamera()

#-------------------------------------------------------------------------------------------------------------
#print
    printString += '////////////////////////////////////////////////////////////////////////////////////////////\n\n'
    #print printString
    #print ('COMPLETE -- check script editor for details...\n')

#*************************************************************************************************************
#*end cameraFrustum()

'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''