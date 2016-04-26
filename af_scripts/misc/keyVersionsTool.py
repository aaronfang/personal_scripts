# This script help set key frame to different versions when review
# key: set visibility key on current time and the neighbour
# <>: these 2 button shift keyframe of selected 1 step forward or backward on timeline
# hide: disconnect keyframe on visibility and hide it.
# Usage:
#   Select one or more objects/groups, then press button

import maya.cmds as cmds
import maya.mel


class keyVersionsTool(object):
    def __init__(self):
        pass
    
    def UI(self,*args):
		if cmds.window("keyVerWin",exists=1):
			cmds.deleteUI("keyVerWin",window=1)
		h=35
		w=250
		w2=50
		
		self.window=cmds.window("keyVerWin",t="Key Versions Tool",s=0,mb=1,rtf=1,w=w,h=h)
		h=cmds.window("keyVerWin",q=1,h=1)
		
		cmds.columnLayout("mainColumn",p="keyVerWin",columnAttach=('both', 2), rowSpacing=10, columnWidth=w)
		cmds.rowLayout("kvRow",p="mainColumn",w=w,numberOfColumns=4,columnWidth4=(w2,30,30,w2),adjustableColumn=1,
		             columnAlign4=[('center'),('center'),('center'),('center')], columnAttach=[(1, 'both', 1), (2, 'both', 0), (3, 'both',0), (4, 'both',5)])
		
		cmds.button(p="kvRow",l="key",c=self.add_key)
		cmds.button(p="kvRow",l="<",c=self.shift_back)
		cmds.button(p="kvRow",l=">",c=self.shift_fwd)
		cmds.button(p="kvRow",l="hide",c=self.rmv_key)
		cmds.showWindow(self.window)
        

    def add_key(self,*args):
    # get selection
        sels = cmds.ls(sl=True,fl=True)

        # set "visibility" on in current frame add off in neighbour
        for sel in sels:
            cur_time = cmds.currentTime(q=True)
            channel = "{0}.visibility".format(sel)
            if cmds.getAttr(channel,k=True):
                cmds.setAttr(channel,0)
                cmds.setKeyframe(channel,t=cur_time-1)
                cmds.setKeyframe(channel,t=cur_time+1)
                cmds.setAttr(channel,1)
                cmds.setKeyframe(channel,t=cur_time)

    def shift_fwd(self,*args):
        # shift keys 1 step fwd
        sels = cmds.ls(sl=True,fl=True)
        for sel in sels:
            channel = "{0}.visibility".format(sel)
            cur_keys = cmds.keyframe(sel,q=True)
            if cur_keys and cur_keys>=1:
                cmds.keyframe(channel,e=True,r=1,tc=1)

    def shift_back(self,*args):
        # shift keys 1 step back
        sels = cmds.ls(sl=True,fl=True)
        for sel in sels:
            channel = "{0}.visibility".format(sel)
            cur_keys = cmds.keyframe(sel,q=True)
            if cur_keys and cur_keys>=1:
                cmds.keyframe(channel,e=True,r=1,tc=-1)
        
    def rmv_key(self,*args):    
        # remove keyframes and hide
        sels = cmds.ls(sl=True,fl=True)
        for sel in sels:
            channel = "{0}.visibility".format(sel)
            maya.mel.eval("CBdeleteConnection {0};".format(channel))
            cmds.setAttr(channel,0)

keyVersionsTool().UI()
