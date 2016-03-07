# generate twigs based on selected curves
# automaticly layout uvs
# rebuild curve to the certain length of one segment
# set root/tip size
# chridren twigs root/tip scale down relatively

# UI
# |   [get curves]      [rebuild] <unit>      |
# |   --------------------------------------  |
# |   root size:<2.5>   tip size:<0.5>        |
# |   relative size: <0.5>-------||---------  |
# |   *random scale <0.1>                     |
# |   *nurbs *polygon                         |
# |                  [apply]                  |
import maya.cmds as cmds


#vars
unit = 2
root_d = 1.5
tip_d = 0.5

# get curves
all_curves = cmds.ls(sl=True,fl=True,type='transform')

# rebuild curves based on length of one segment
for curve in all_curves:
    # get curve length
    length = cmds.arclen(curve)
    segment = int(length/unit)
    cmds.rebuildCurve(curve,s=segment,d=3,ch=0)

# create root/tip circles based on parameters
root_circle = cmds.circle(n='root_circle',c=(0,0,0),nr=(0,1,0),r=(root_d/2),d=3,ch=1,s=6)
# extrude -ch true -rn false -po 0 -et 2 -ucp 0 -fpt 1 -upn 1 -rotation 0 -scale 1 -rsp 1 "root_circle" "curve1" ;
# setAttr "extrude1.scale" 0.1;
