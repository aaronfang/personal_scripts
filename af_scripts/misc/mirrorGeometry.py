import maya.cmds as cmds

class MirrorObj(object):
    def __init__(self):
        pass

    def _UI(self,*args):
        pass

    def renameDup(self,org_obj):
        if org_obj:
            if "L_" in org_obj and "left" not in org_obj and "right" not in org_obj:
                mirrored_obj="R_{0}".format(org_obj.split('L_')[1])
                return mirrored_obj
            elif "R_" in org_obj and "left" not in org_obj and "right" not in org_obj:
                mirrored_obj="L_{0}".format(org_obj.split('R_')[1])
                return mirrored_obj
            elif "L_" in org_obj and "left" in org_obj and "right" not in org_obj:
                mirrored_obj="R_{0}right{1}".format(org_obj.split('L_')[1].split('left')[0],org_obj.split('L_')[1].split('left')[1])
                return mirrored_obj
            elif "L_" in org_obj and "left" not in org_obj and "right" in org_obj:
                mirrored_obj="R_{0}left{1}".format(org_obj.split('L_')[1].split('right')[0],org_obj.split('L_')[1].split('right')[1])
                return mirrored_obj
            elif "R_" in org_obj and "left" in org_obj and "right" not in org_obj:
                mirrored_obj="L_{0}right{1}".format(org_obj.split('R_')[1].split('left')[0],org_obj.split('R_')[1].split('left')[1])
                return mirrored_obj
            elif "R_" in org_obj and "left" not in org_obj and "right" in org_obj:
                mirrored_obj="L_{0}left{1}".format(org_obj.split('R_')[1].split('right')[0],org_obj.split('R_')[1].split('right')[1])
                return mirrored_obj
            elif "M_" in org_obj and "left" not in org_obj and "right" in org_obj:
                mirrored_obj="{0}left{1}".format(org_obj.split('right')[0],org_obj.split('right')[1])
                return mirrored_obj
            elif "M_" in org_obj and "left" in org_obj and "right" not in org_obj:
                mirrored_obj="{0}right{1}".format(org_obj.split('left')[0],org_obj.split('left')[1])
                return mirrored_obj
            else:
                mirrored_obj="Mirrored_{0}".format(org_obj)
                return mirrored_obj

    def doMirror(self,*args):

# mirror objs
objs = cmds.ls(sl=True,fl=True,tr=True);

for obj in objs:
    cur_center = cmds.objectCenter(obj)
    bbox = cmds.xform(obj,q=True,bb=True)
    cur_piv = cmds.xform(obj,q=True,ws=True,piv=True)[:3]
    origin = [0,0,0]

    dup_node = cmds.duplicate(obj,n=self.renameDup(obj))
    cmds.scale(-1,1,1,dup_node,p=origin,ws=True,r=True)
    cmds.xform(dup_node,ws=True,piv=origin)

    cmds.polyNormal(dup_node,nm=0,ch=0)
    cmds.select(d=True)
