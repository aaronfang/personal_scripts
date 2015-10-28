# strip multi-shapes from transfrom node
curSel = cmds.ls(sl=1,dag=1,lf=1)
for shape in curSel:
	trans = cmds.group(em=1,n=shape.split('|')[1])
	cmds.parent(shape,trans,r=1,s=1)
