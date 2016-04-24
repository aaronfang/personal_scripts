from pymel.core import *
import maya.mel as mel 

deleteUI('unifiedRenderGlobalsWindow')
mel.eval('buildNewSceneUI;')
