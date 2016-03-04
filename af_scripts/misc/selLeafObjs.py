import maya.cmds as cmds

def selLeafObjs():
    curSel = cmds.ls(sl=1,fl=1)[0]
    cmds.select(curSel,hi=1)
    chirdrenShape = cmds.ls(sl=1,fl=1,s=1)
    trans = cmds.listRelatives(chirdrenShape,p=1,f=1)
    cmds.select(trans,r=1)
selLeafObjs()
