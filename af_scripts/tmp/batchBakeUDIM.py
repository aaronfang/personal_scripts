# BAKE UDIM TILES
#
# ====================================================================================================================
# Description: Bake out multiple tiles using Batch Bake (Mental Ray).
#
# ====================================================================================================================
# Usage: Two methods. First is quick and simple but temporary. Second installs
#        the script so you can use it regularly.
#
# ====================================================================================================================
# Method 1: Copy and paste the contents of script to a Python tab inside
#		the script editor. Select all the code and execute it (using Enter on keypad).
#		Now all you need to do is run the following command:
#		
#			bakeTiles()
#			
#		In a python script editor tab.
#
# ====================================================================================================================		
# Method 2: Copy the file to your Maya user scripts directory (See section on "User Scripts Path" below for details).
#			
#		In your user scripts directory, add the following line to your userSetup.py...
#			
#			import bakeUDimTiles as bt
#
#		Note: If userSetup.py doesn't exist, create a textfile, insert the above line and save it as userSetup.py		
#			
#		Reopen Maya and you can run the script using the following command in the python script editor:
#		
#			bt.bakeTiles()
#			
# ====================================================================================================================		
# Arguments: The command by default tries to figure out what camera to use as well as what
#			shading group and bake set the selected object/s are connected to.
#			The following arguments can be used to override the defaults:
#
#				camera = <name of camera transform> ie... persp, top, front, side, renderCam
#				shadingGroup = <name of shading group> ie... initialShadingGroup, lambert2ShadingGroup
#				bakeSet = <name of textureBakeSet> ie... initialTextureBakeSet, occlusionBakeSet
#
#			For example...
#				
#				bakeTiles(camera='renderCam', shadingGroup='myShadingGroup', bakeSet='occlusionBakeSet')
#
# ===================================================================================================================
# User Scripts Path: These are default script paths used by Maya.
#
#			Where <mayaversion> is the version of Maya your using. The difference between the two
#			locations is the first is available only to that version of Maya, while the second is
#			available to all versions of Maya.
#			
#			On Windows:
#				<user directory>/My Documents/maya/<mayaversion>/scripts
#				<user directory>/My Documents/maya/scripts 
#			On Mac:
#				In your Home folder, under Library/Preferences/Autodesk/maya/<mayaversion>
#				In your Home folder, under Library/Preferences/Autodesk/maya
#			On Linux:
#				In your Home folder, under maya/<mayaversion>/scripts
#				In your Home folder, under maya/scripts
#
#			For more information about user script locations, see the doc's under "File Path Variables"
#				
				

from pymel.core import *
import math as m

def removeDuplicates(seq):
	# Not order preserving    
	myset = set(seq)
	return list(myset)

def processLightMaps(tiles, camera, bakeSet, bakeGroup, bakeObject):
	import maya.mel as mel
	myBakeSet = ls (bakeSet, type='textureBakeSet')
	myBakeSet[0].uvRange.set(2)
	for i in tiles:
		rawid = i-1001
		tu = int (rawid % 10)
		tv = int (m.floor(rawid/10))
		myBakeSet[0].prefix.set('baked_%s' % str(i))
		myBakeSet[0].uMin.set(tu)
		myBakeSet[0].uMax.set(tu+1)
		myBakeSet[0].vMin.set(tv)
		myBakeSet[0].vMax.set(tv+1)
		mel.eval( 'convertLightmap -camera %s -bo %s %s %s' % (camera, bakeSet, bakeGroup, bakeObject) )

def getTiles(bakeObject):
	import pymel.core.runtime as pyrt
	udims = []
	select (bakeObject)
	sizeUVs = polyEvaluate (uv=True)
	pyrt.ConvertSelectionToUVs()
	getUVs = ls(sl=True, fl=True)
	removeUVs = getUVs
	
	while (sizeUVs > 0):
		select (removeUVs[0])
		pyrt.SelectUVShell()
		shellUVs = ls (sl=True, fl=True)
		UVs = polyEvaluate (bc2=True)
		SS = m.floor (UVs[0][0])
		TT = m.floor (UVs[1][0])
		TT = m.fabs (TT)
		udim = int (TT * 10 + SS + 1001)
		udims.append(udim)
		removeUVs = list (set(removeUVs) - set(shellUVs))
		sizeUVs = len(removeUVs)
	return removeDuplicates (udims)

def checkBakeSet(bakeSet):
	status = True
	if objExists(bakeSet) == False:
		print("Warning: no bakeset exists with that name!")
		status = False
	return status

def getBakeConnection(myObj):
	status = False
	lsShape = myObj.getShape()
	lsConnections = lsShape.outputs()
	for i in lsConnections:
		if i.type() == 'textureBakeSet':
			status = i.name()
	if status == False:
		print 'not connected to bake set'
	return status


def getSGConnection(myObj):
	status = False
	lsShape = myObj.getShape()
	lsConnections = lsShape.outputs()
	for i in lsConnections:
		if i.type() == 'shadingEngine':
			status = i.name()
	if status == False:
		print 'not connected to shading group'
	return status

def bakeTiles(camera='persp', shadingGroup=False, bakeSet=False):
	selectedObjects = ls (sl=True, fl=True)
	for myObj in selectedObjects:
		if bakeSet == False:
			bakeSet = getBakeConnection(myObj)
		if shadingGroup == False:
			shadingGroup = getSGConnection(myObj)
		if bakeSet != False or shadingGroup != False or checkBakeSet(bakeSet) != False:
			tiles = getTiles (myObj)
			processLightMaps(tiles, camera, bakeSet, shadingGroup, myObj)
	select (selectedObjects)