import pymel.core as pm

def set_pivot_to_selected_face(face):
    cur_sel = pm.select(face,r=1)
    if cur_sel and len(cur_sel) == 1 and cur_sel.split(:
        pm.mel.eval("setToolTo Move;")
        piv = pm.manipMoveContext("Move",q=1,p=1)
        mesh = pm.listRelatives(pm.listRelatives(face,p=1)[0],p=1)
        vtx = pm.ls(pm.polyListComponentConversion(face,tv=1),fl=1)
        if len(vtx)>=3:
            planeA = pm.polyPlane(w=1,h=1,sx=1,sy=1,ax=[0,1,0],cuv=2,ch=1,n="rotationPlaneA")[0]
            pm.select("{0}.vtx[0:2]".format(planeA),vtx[0:3],r=1)
            pm.mel.eval("snap3PointsTo3Points(0);")
            pm.parent(mesh,planeA)

            pm.xform(planeA,ws=1,piv=(piv[0],piv[1],piv[2]))

            cur_plane_pos = pm.xform(planeA,q=True,ws=True,piv=True)[0:3]
            cur_plane_rot = pm.xform(planeA,q=True,ws=True,ro=True)

            pm.parent(mesh,w=1)
            pm.select(mesh,planeA,r=1)
            pm.makeIdentity(a=1,t=1,r=0,s=0,n=0)
            pm.parent(mesh,planeA)

            pm.xform(planeA,ws=True,t=(-cur_plane_pos[0],-cur_plane_pos[1],-cur_plane_pos[2]),ro=(0,0,0))

            pm.parent(mesh,w=1)
            pm.select(mesh,planeA,r=1)
            pm.makeIdentity(a=1,t=1,r=1,s=0,n=0)
            pm.parent(mesh,planeA)
            pm.xform(planeA,ws=True,t=(cur_plane_pos[0],cur_plane_pos[1],cur_plane_pos[2]),ro=(cur_plane_rot[0],cur_plane_rot[1],cur_plane_rot[2]))

            pm.xform(mesh,ws=1,piv=(piv[0],piv[1],piv[2]))

            pm.parent(mesh,w=1)
            pm.delete(planeA)

def get_selection():
get_sel = pm.ls(sl=1)
set_pivot_to_selected_face(get_sel)

for x in pm.ls(os=1,fl=1):
    face="{0}.f[154]".format(x)
    set_pivot_to_selected_face(face)
    
