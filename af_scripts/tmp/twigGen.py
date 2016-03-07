# generate twigs based on selected curves
# automaticly layout uvs
# rebuild curve to the certain length of one segment
# set root/tip size
# chridren twigs root/tip scale down relatively

# UI
# |   [get curves]      [rebuild] <density>   |
# |   --------------------------------------  |
# |   root size:<2.5>   tip size:<0.5>        |
# |   relative size: <0.5>-------||---------  |
# |   *random scale <0.1>                     |
# |   *nurbs *polygon                         |
# |                  [apply]                  |
import maya.cmds as cmds


# get curves
all_curves = cmds.ls(sl=True,fl=True,type='curve')

# rebuild curves based on length of one segment
for curve in all_curves:
    # get curve length
    cmds.curve(
