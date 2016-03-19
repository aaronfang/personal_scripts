# Python Version
def flipMesh():
    sel=cmds.ls(sl=1)
    axis={'x':0,'y':1,'z':2}
    reverse=[1.0,1.0,1.0]
    #quring the axtive symmetry axis
    activeaxis=cmds.symmetricModelling(q=1, axis=1)
    reverse[axis[activeaxis]]=-1.0
    #getting the vertex count
    verts=cmds.polyEvaluate(v=1)
    #selecting all vertex
    cmds.select(sel[0]+'.vtx[0:'+str(verts)+']')
    #getting all the positive vertex
    posit=cmds.filterExpand(sm=31,ex=1,smp=1)
    seam=cmds.filterExpand(sm=31,ex=1,sms=1)
    #swapping position on the positive side with the negative side
    for pos in posit:
       cmds.select(pos, sym=True)
       neg=cmds.filterExpand(sm=31,ex=1,smn=1)
       posT=cmds.xform(pos, q=1, t=1)
       negT=cmds.xform(neg[0], q=1, t=1)
       cmds.xform(pos,t=[a*b for a,b in zip(negT,reverse)])
       cmds.xform(neg[0],t=[a*b for a,b in zip(posT,reverse)]) 
    #inverting position on the seam
    for each in seam:      
      seamP=cmds.xform(each, q=1, t=1)
      seaminvP=[a*b for a,b in zip(seamP,reverse)]
      cmds.xform(each, t=(seaminvP))
    cmds.select(sel)



# API Version
# Here's an example that will simply mirror all points of a selected object along their z axis:
import maya.OpenMaya as OpenMaya

# Get selected object
mSelList = OpenMaya.MSelectionList()
OpenMaya.MGlobal.getActiveSelectionList(mSelList)
sel = OpenMaya.MItSelectionList(mSelList)
path = OpenMaya.MDagPath()
sel.getDagPath(path)

# Attach to MFnMesh
MFnMesh = OpenMaya.MFnMesh(path)

# Create empty point array to store new points
newPointArray = OpenMaya.MPointArray()

for i in range( MFnMesh.numVertices() ):
    # Create a point, and mirror it
    newPoint = OpenMaya.MPoint()
    MFnMesh.getPoint(i, newPoint)
    newPoint.z = -newPoint.z
    newPointArray.append(newPoint)

# Set new points to mesh all at once
MFnMesh.setPoints(newPointArray)