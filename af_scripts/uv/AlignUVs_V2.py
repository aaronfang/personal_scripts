import maya.cmds as cmds
import math


def lineup_U_in_UDIM():
    sels = cmds.ls(os=1)
    gap_w = 0.07
    gap_h = 0.01
    initGap = 0.003
    UDIM_limit = 10
    fst_in_UDIM = 0

    for i, x in enumerate(sels):
        cmds.select('{0}.map[:]'.format(x), r=1)

        if i == 0:
            # move to the init place
            cmds.polyEditUV(u=-cmds.polyEvaluate(x, b2=1)[0][0] + initGap, v=-cmds.polyEvaluate(x, b2=1)[1][0] + initGap)

        elif i >= 1:
            # get the size of the last shell
            w_last = cmds.polyEvaluate(sels[i-1], b2=1)[0][1]-cmds.polyEvaluate(sels[i-1], b2=1)[0][0]
            # h_last = cmds.polyEvaluate(sels[i-1], b2=1)[1][1]-cmds.polyEvaluate(sels[i-1], b2=1)[1][0]
            # calc the distance to the last shell
            dist_u = cmds.polyEvaluate(x, b2=1)[0][0]-cmds.polyEvaluate(sels[i-1], b2=1)[0][0]
            dist_v = cmds.polyEvaluate(x, b2=1)[1][0]-cmds.polyEvaluate(sels[i-1], b2=1)[1][0]
            # move current shell to the last shell
            cmds.polyEditUV(u=-dist_u+w_last+gap_w, v=-dist_v)
            # get the UDIM ID of the current shell and the last shell
            UDIM = int((math.floor(cmds.polyEvaluate(x, b2=1)[0][1])+1)+(math.floor(cmds.polyEvaluate(x, b2=1)[1][1])*10))
            UDIM_last = int((math.floor(cmds.polyEvaluate(sels[i-1], b2=1)[0][1])+1)+(math.floor(cmds.polyEvaluate(sels[i-1], b2=1)[1][1])*10))
            # if shell U is out of UDIM
            if UDIM-UDIM_last==1:
                new_u = -(cmds.polyEvaluate(x, b2=1)[0][0]-initGap)+(UDIM-2)
                new_v = -(cmds.polyEvaluate(x, b2=1)[1][0]-cmds.polyEvaluate(sels[fst_in_UDIM:i], b2=1)[1][1])+gap_h
                cmds.polyEditUV(u=new_u, v=new_v)
                # if shell V is out of UDIM
                if int((math.floor(cmds.polyEvaluate(x, b2=1)[0][1])+1)+(math.floor(cmds.polyEvaluate(x, b2=1)[1][1])*10))-UDIM_last==10:
                    fst_in_UDIM = i
                    new2_u = -(cmds.polyEvaluate(x, b2=1)[0][0]-initGap)+(int((math.floor(cmds.polyEvaluate(x, b2=1)[0][1])+1)+(math.floor(cmds.polyEvaluate(x, b2=1)[1][1])*10))-UDIM_limit)
                    new2_v = -cmds.polyEvaluate(x, b2=1)[1][0] + initGap
                    cmds.polyEditUV(u=new2_u, v=new2_v)
    cmds.select(sels, r=1)
