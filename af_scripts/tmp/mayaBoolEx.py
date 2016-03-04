import maya.cmds as cmds

# create bbox for the hidden transform nodes
trans_nodes = cmds.ls(sl=True,fl=True)
for node in trans_node:
    bbox = cmds.xform(node,q=True,bb=True)
    w = ( bbox[3] - bbox[0] )
    h = ( bbox[4] - bbox[1] )
    d = ( bbox[5] - bbox[2] )
    x = ( bbox[3] + bbox[0] ) / 2.0
    y = ( bbox[4] + bbox[1] ) / 2.0
    z = ( bbox[5] + bbox[2] ) / 2.0
    
    # create a curve box at origin size 1,1,1
    pos =  [[-0.5, 0.5, -0.5],[-0.5, 0.5, 0.5],[0.5, 0.5, 0.5],
     [0.5, 0.5, -0.5],[-0.5, 0.5, -0.5],[-0.5, -0.5, -0.5],
     [0.5, -0.5, -0.5],[0.5, 0.5, -0.5],[0.5, 0.5, 0.5],
     [0.5, -0.5, 0.5],[0.5, -0.5, -0.5],[-0.5, -0.5, -0.5],
     [-0.5, -0.5, 0.5],[0.5, -0.5, 0.5],[0.5, 0.5, 0.5],
     [-0.5, 0.5, 0.5],[-0.5, -0.5, 0.5]]
    cv_box = cmds.curve(p=pos,per = False, d=1, k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])
    
    # 
