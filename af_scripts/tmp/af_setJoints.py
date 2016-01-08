import pymel.core as pm

curSel = pm.ls(sl=True,type='transform')[0]

bBox = pm.xform(curSel,ws=1,q=1,bb=1)
sizeX = abs(bBox[0]-bBox[3])
sizeY = abs(bBox[1]-bBox[4])
sizeZ = abs(bBox[2]-bBox[5])
curPvt = [(bBox[0]+sizeX/2),(bBox[1]+sizeY/2),(bBox[2]+sizeZ/2)]

ccUD = pm.circle(n='circle_rotUpDown',r=sizeY/2,nr=(1,0,0))
pm.move(ccUD[0],curPvt)

ccLR = pm.circle(n='circle_rotLeftRight',r=sizeX/2,nr=(0,1,0))
pm.move(ccLR[0],curPvt)

pm.select(d=1)
pm.jointDisplayScale(0.1)
pm.joint(p=(0,bBox[1],bBox[2]),n='joint_base')
pm.joint(p=(pm.xform(ccUD,ws=1,q=1,rp=1)),n='joint_rotUpDown')
pm.joint(p=(pm.xform(ccLR,ws=1,q=1,rp=1)),n='joint_rotLeftRight')
