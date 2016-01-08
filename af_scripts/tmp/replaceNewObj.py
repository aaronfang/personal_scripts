orgM = cmds.ls(sl=1,fl=1)
newM = cmds.ls(sl=1,fl=1)

for nm in newM:
	for om in orgM:
		if nm.split(':')[0] == om.split(':')[0]+'1':
			trans = cmds.xform(om,ws=1,piv=1,q=1)
			rot = cmds.xform(om,ws=1,ro=1,q=1)
			cmds.xform(nm,t=trans[0:3],ro=rot)
			cmds.namespace(ren=((nm.split(':')[0]),(nm.split(':')[1])))
