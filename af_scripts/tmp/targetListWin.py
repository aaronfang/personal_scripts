import maya.cmds as cmds
import maya.mel as mm

objs = cmds.ls(sl=True,fl=True)

blendshape_node = cmds.blendShape(objs[0:-1],objs[-1],n="{0}_blendshape".format(objs[-1]))
if len(blendshape_node)>0:
    for obj in objs[0:-1]:
        cmds.setAttr("{0}.visibility".format(obj),False)

target_nodes = cmds.blendShape(blendshape_node[0],q=True,t=True)
target_weights = cmds.blendShape(blendshape_node[0],q=True,w=True)

if len(target_nodes)>0:
    w = 300
    if cmds.window('blendshapeWin',exists=True):cmds.deleteUI('blendshapeWin',window=True)
    cmds.window('blendshapeWin',t='BlendShape Editor',w=w,rtf=1,mxb=0,mnb=0,s=0)
    #cmds.columnLayout("mainColumn",p="blendshapeWin",columnAttach=('both', 2), rowSpacing=10, columnWidth=w)
    cmds.rowColumnLayout('mainRowColumn',p='blendshapeWin',numberOfColumns=3, columnWidth=[(1, 100), (2, 150), (3, 50)] )
    for i,tgt in enumerate(target_nodes):
        cmds.text(p='mainRowColumn',l=tgt)
        cmds.floatSlider("{0}FltSld".format(tgt),p='mainRowColumn',v=target_weights[i],max=1,min=0)
        cmds.button(p='mainRowColumn',l='Edit')
    cmds.showWindow('blendshapeWin')

def changeTargetValue():
cmds.floatSlider(
cmds.blendshape(


def editBlendShape():
cmds.
