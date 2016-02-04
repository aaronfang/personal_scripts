import pymel.core as pm

pm.mel.eval("setToolTo Move;")
piv = pm.manipMoveContext("Move",q=1,p=1)
get_sel = pm.ls(sl=1,fl=1)
mesh = pm.listRelatives(pm.listRelatives(get_sel[0],p=1)[0],p=1)
vtx = pm.ls(pm.polyListComponentConversion(get_sel[0],tv=1),fl=1)
if len(vtx)>=3:
	c_plane = pm.polyPlane(w=1,h=1,sx=1,sy=1,ax=[0,1,0],cuv=2,ch=1,n="rotationPlane")[0]
	pm.select("{0}.vtx[0:2]".format(c_plane),vtx[0:3])
	pm.mel.eval("snap3PointsTo3Points(0);")
	pm.parent(mesh,c_plane)
	tmp = []
	for a in ("{0}.tx,{0}.ty,{0}.tz,{0}.rx,{0}.ry,{0}.rz,".format(c_plane)):
		tmp.append(a)
		pm.setAttr(a,0)
	pm.makeIdentity(mesh,a=1,t=0,r=1,s=0,n=0)
	pm.xform(mesh,ws=1,piv=(piv[0],piv[1],piv[2]))
	for i,a in enumerate("{0}.tx,{0}.ty,{0}.tz,{0}.rx,{0}.ry,{0}.rz,".format(c_plane)):
		pm.setAttr(a,tmp[i])
	pm.parent(mesh,w=1)
	pm.delete(c_plane)
