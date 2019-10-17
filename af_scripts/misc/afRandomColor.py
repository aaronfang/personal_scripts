import maya.cmds as mc
import random

def afRandomColor():
    
    objs = mc.ls(sl=1,fl=1)
    
    for obj in objs:
        mats = mc.ls(mat=1,fl=1)
        if not ((obj+'_mat')) in mats:
            mat = mc.shadingNode('lambert',n=(obj+'_mat'),asShader=1)
            mc.setAttr((mat+".color"),random.random(),random.random(),random.random(),type='double3')
            mc.select(obj,r=1)
            mc.hyperShade(assign=mat)
            mc.select(cl=1)
        else:
            mc.setAttr((obj+"_mat.color"),random.random(),random.random(),random.random(),type='double3')
    mc.select(objs,r=1)

afRandomColor()
