# Add objects from selected deformer
curSel = cmds.ls(sl=1,fl=1)
for sel in curSel[0:-1]:
	cmds.deformer(curSel[-1],e=1,g=sel)


# Remove objects from selected deformer
curSel = cmds.ls(sl=1,fl=1)
for sel in curSel[0:-1]:
	cmds.deformer(curSel[-1],e=1,g=sel,rm=1)
