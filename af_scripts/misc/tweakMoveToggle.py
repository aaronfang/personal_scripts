# -----------------------------------------------------
# Set tool to "object" mode with marquee turned on
# Set tool to "vtx" mode with tweak turned on
import maya.cmds as cmds
import maya.mel as mel


if cmds.selectMode(q=True,co=True):
    cmds.selectMode(o=True)
    mel.eval('setToolTo $gSelect')
    mel.eval('dR_DoCmd("selectModeDisableTweakMarquee")')
    mel.eval('dR_DoCmd("selectModeMarquee")')
elif cmds.selectMode(q=True,o=True):
    cmds.selectMode(co=True)
    cmds.selectType(pv=True)
    mel.eval('setToolTo $gMove')
    mel.eval('dR_DoCmd("selectModeTweakMarquee")')
    mel.eval('dR_setActiveTransformAxis 3;')


# -----------------------------------------------------
# mel command
# dR_setActiveTransformAxis 0;//x
# dR_setActiveTransformAxis 1;//y
# dR_setActiveTransformAxis 2;//z
# dR_setActiveTransformAxis 3;//xyz
# dR_setActiveTransformAxis 4;//xy
# dR_setActiveTransformAxis 5;//yz
# dR_setActiveTransformAxis 6;//xz
