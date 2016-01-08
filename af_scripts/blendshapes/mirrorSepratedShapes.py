### This script works for separacted shapes. Made by Edwin NG
### 
### 1,Select good shape first then select the target shape
### 2,Run this cmd.
import maya.cmds as cmds
def mirrorSepratedShapes():
   
	geo = cmds.ls(sl=1,fl=1)
	
	if 'L_' in geo[0]:
	    print 'Mirroring from Left to Right'
	    side='left'
	    Lgeo=geo[0]
	    Rgeo=Lgeo.replace('L_', 'R_')
	   
	if 'R_' in geo[0]:
	    print 'Mirroring from Right to Left'
	    side='right'
	    Rgeo=geo[0]
	    Lgeo=Rgeo.replace('R_', 'L_')     
	 
	Lshape=cmds.listRelatives(Lgeo, shapes=True, type='mesh', ni=True)
	Rshape=cmds.listRelatives(Rgeo, shapes=True, type='mesh', ni=True)
	
	Lvert=cmds.polyEvaluate(Lshape[0], v=True)
	Rvert=cmds.polyEvaluate(Rshape[0], v=True) 
	
	if not Lvert==Rvert:
	    print 'Vertex count not matching between the two sides'
	   
	if side=='left':
	    base=Lgeo
	    target=Rgeo
	   
	if side=='right':
	    base=Rgeo
	    target=Lgeo
	
	for i in range(0,Lvert):
	    #print('%s.vtx[%d]'%(Lgeo,i))
	    pos=cmds.xform(('%s.vtx[%d]'%(base,i)), q=True, ws=True, t=True)
	    cmds.xform(('%s.vtx[%d]'%(target,i)), t=((pos[0]*-1),pos[1],pos[2]), ws=True)
mirrorSepratedShapes()
