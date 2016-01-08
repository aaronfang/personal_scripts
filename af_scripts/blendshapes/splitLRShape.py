#####################################################

# Made by Jeff Rosenthal
# JeffRosenthal.org
# 8/1/2012
################################################################################
# Creates left and ride side variations of a blendshape along the X axis
#
# Select your source face, then select the blendshape you created
# run the script!
#
# Questions? jeffrosenth at gmail dot com


#USER CAN CHANGE THIS NUMBER
###################
percentRange = .1

####  .1 = 10% falloff
####  .3 = 30% falloff
####   1 = 100% falloff (probably looks bad)
###################


import maya.cmds as cmds

def getValue(x, range, max):
       value = (1 - x / (range * max)) / 2
       return clamp(value, 0, 1)

def clamp(value, low, high):
    if value < low:
        return low
    if (value > high):
        return high
    return value
       
def getShapeNode(transform):
    return cmds.listRelatives(transform, shapes=True)[0]

def splitLRShape():
	(sourceObj, targetObj) = cmds.ls(sl=1)
	sourceShape = getShapeNode(sourceObj)

	#look at number of verticies
	cmds.select(sourceObj)
	numVerts = cmds.polyEvaluate(v=1)

	#figure out width of face (assume X axis)
	rgtX = 0
	lftX = 0
	for i in range(0,numVerts):
		   testX = cmds.pointPosition(targetObj + ".vtx[" + str(i) + "]", l=1)[0]
		   if testX < rgtX:
		           rgtX = testX
		   if testX > lftX:
		           lftX = testX
		           
	#duplicate face twice (one left, one right)
	cmds.select(targetObj)
	targetObj_Lft = cmds.duplicate(n=targetObj+'_Lft')[0]
	cmds.move(rgtX * -2.1, 0, 0, r=1)
	cmds.select(targetObj)
	targetObj_Rgt = cmds.duplicate(n=targetObj+'_Rgt')[0]
	cmds.move(rgtX * 2.1, 0, 0, r=1)

	side = 1
	#on each object
	for target in ([targetObj_Lft, targetObj_Rgt]):
		side *= -1
		#for each vert
		for i in range(0,numVerts):
		    #get vert positions
		    #sourcePos = cmds.getAttr(sourceShape + '.pnts[' + str(i) + ']')[0]
		    #targetPos = cmds.getAttr(target + '.pnts[' + str(i) + ']')[0]
		    sourcePos = cmds.pointPosition(sourceObj + ".vtx[" + str(i) + "]", l=1)
		    targetPos = cmds.pointPosition(target + ".vtx[" + str(i) + "]", l=1)        
		    
		    #find difference
		    differencePos = (sourcePos[0] - targetPos[0], sourcePos[1] - targetPos[1], sourcePos[2] - targetPos[2])
		    
		    #get falloff amount from side of object
		    testX = cmds.pointPosition(sourceObj + ".vtx[" + str(i) + "]", l=1)[0]
		    falloff = getValue(testX, percentRange, rgtX * side)
		    
		    #move vert difference * falloff amount
		    cmds.xform(target + '.vtx[' + str(i) + ']', rt=(differencePos[0] * falloff, differencePos[1] * falloff, differencePos[2] * falloff))

	cmds.select(cl=True)
splitLRShape()
