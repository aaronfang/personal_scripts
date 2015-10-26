# remove specific uv set on selected meshes.
setName = 'uvSet'
curSel = cmds.ls(sl=1,fl=1)
for sel in curSel:
	for uset in cmds.polyUVSet(sel,auv=1,q=1):
		if uset == setName:
			cmds.polyUVSet(sel,uvSet=setName,d=1)
