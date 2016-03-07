import maya.cmds as cmds


# select source then select targets run the following
def replaceNodes():
    sels = cmds.ls(sl=1,fl=1,type='transform')
    source = sels[0]
    targets = sels[1:]

    for i,tgt in enumerate(targets):
        t = cmds.xform(tgt,ws=True,q=True,t=True)
        r = cmds.xform(tgt,ws=True,q=True,ro=True)
        s = cmds.xform(tgt,ws=True,q=True,s=True)
        dup_src = cmds.duplicate(source,n="{0}_copy{1}".format(source,i+1))
        cmds.xform(dup_src[0],ws=True,t=t,ro=r,s=s)
        cmds.setAttr("{0}.visibility".format(tgt),0)
replaceNodes()
