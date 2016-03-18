import random
import maya.mel


class distributeOnSurface(object):
    
    def __init__(self):
        pass
    
    def _UI(self):
        if cmds.window('dosWin',exists=True):
            cmds.deleteUI('dosWin',window=True)
        w=300
        w2=180
        cmds.window('dosWin',t="Distribute On Surface",s=0,rtf=1,mb=1,mxb=0,mnb=0,w=w)
        cmds.columnLayout("mainColumn",p="BSMainWin",columnAttach=('both', 2), rowSpacing=10, columnWidth=w)
        
        cmds.rowLayout("srcTgtNamesRow",p="mainColumn",w=w,numberOfColumns=3,columnWidth3=(w2,30,w2),
                       adjustableColumn=2, columnAlign3=[('center'),('center'),('center')],
                       columnAttach=[(1, 'both', 1), (2, 'both', 0), (3, 'both',5)])
        cmds.textScrollList("srcList",p="srcTgtNamesRow",w=w2,numberOfRows=1, allowMultiSelection=False)
        pm.popupMenu("srcListPopUp",p="srcList")
        pm.menuItem(p="srcListPopUp",l="Add Source Geo",c=self.srcList)
        
        cmds.textScrollList("tgtList",p="srcTgtNamesRow",w=w2,numberOfRows=1, allowMultiSelection=False)
        pm.popupMenu("tgtListPopUp",p="tgtList")
        pm.menuItem(p="tgtListPopUp",l="Add Base Geo",c=self.tgtList)
        
        cmds.showWindow('dosWin')



src_obj = 'pCone1'
tgt_obj = 'pPlane1'
del_trans = [cmds.delete(x) for x in cmds.ls(sl=True,fl=True,dag=1,lf=1) if cmds.nodeType(x) != 'follicle']
fols = [x for x in cmds.ls(sl=True,fl=True,dag=1,lf=1) if cmds.nodeType(x) == 'follicle']
cmds.select(fols,r=1)
maya.mel.eval('randomizeFollicles 0.05')

rand_uv = 0.05
rand_l = 0.5
rand_offset = 1

dup_objs = []
for fol in fols:
    dup_obj = pm.duplicate(src_obj,n='{0}_dup'.format(src_obj))[0]
    dup_objs.append(dup_obj)
    pm.parent(dup_obj,fol)
    for attr in ['tx','ty','tz','rx','ry','rz']:
        pm.setAttr('{0}.{1}'.format(dup_obj,attr),0)

# Random length 
for obj in dup_objs:
    lenght_var = random.uniform(-rand_l,rand_l)
    pm.setAttr('{0}.sz'.format(obj),(1+lenght_var))

# Random offset
for obj in dup_objs:
    offset_var = random.uniform(-rand_offset,rand_offset)
    pm.setAttr('{0}.tz'.format(obj),(offset_var))
