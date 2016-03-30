# -----------------------------------------------------
# Set tool to "object" mode with marquee turned on
# Set tool to "vtx" mode with tweak turned on
import maya.cmds as cmds
import maya.mel as mel


if cmds.selectMode(q=True,co=True):
    cmds.selectMode(o=True)
    mel.eval('dR_DoCmd("selectModeDisableTweakMarquee")')
    mel.eval('dR_DoCmd("selectModeMarquee")')
elif cmds.selectMode(q=True,o=True):
    cmds.selectMode(co=True)
    cmds.selectType(pv=True)
    mel.eval('dR_DoCmd("selectModeTweakMarquee")')
