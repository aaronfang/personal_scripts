### This script works for separacted shapes. Made by Edwin NG
### 
### 1,create onside geo (name have to be "R_"/"L_")
### 2,dup and rename to the oppesite (R>L or L>R)
### 3,select both geos set transforms to origin
### 4,run the script except last line
### 5,select on3eside is correct,run last line. Done.
### I will modify it to use more easy.

def mirrorEyelash(geo=None):
   
      
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
       
mirrorEyelash(geo=cmds.ls(sl=True))
