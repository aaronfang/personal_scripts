import maya.cmds as cmds
import maya.mel as mel
cmds.select(cmds.ls('*:*.faceCtrl', o=1))
mel.eval('doSetKeyframeArgList 6 { "4","0","0","0","1","0","0","animationList","0","1","0" };')
