def setToOrigin():
    objs = cmds.ls(sl=True,fl=True,type="transform")
    for obj in objs:
        cmds.select(obj,r=1)
        cmds.makeIdentity(a=True,t=1,r=1,s=1)
        bbox = cmds.xform(obj,ws=True,q=True,bb=True)
        oc = cmds.objectCenter(obj)
        cmds.move(-oc[0],-bbox[1],-oc[2],obj,ws=True,xyz=True)
        cmds.xform(obj,ws=True,piv=(0,0,0))
        cmds.makeIdentity(a=True,t=1,r=1,s=1)
        cmds.delete(obj,ch=True)
setToOrigin()
