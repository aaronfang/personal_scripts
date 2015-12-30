# Store XFormation
grpNma = cmds.ls(sl=True,type='transform')[0]
grpTa = cmds.xform(grpNma,ws=1,piv=1,q=1)
grpRa = cmds.xform(grpNma,ws=1,ro=1,q=1)
# grpSa = cmds.xform(grpNma,ws=1,s=1,q=1)


# xform
grpNmb = cmds.ls(sl=True,type='transform')[0]
cmds.xform(grpNmb,ws=1,t=(grpTa[0],grpTa[1],grpTa[2]))
cmds.xform(grpNmb,r=1,ro=(grpRa[0],grpRa[1],grpRa[2]))
# cmds.xform(grpNmb,s=1,sp=(grpSa[0],grpSa[1],grpSa[2]))
# test