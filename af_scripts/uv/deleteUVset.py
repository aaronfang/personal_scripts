from maya import cmds

class deleteUVset(object):

    def __init__(self):
        self.setNameFld = None
        self.window = ""

    def _UI(self):
    	if cmds.window(self.window,exists=1):
    		cmds.deleteUI(self.window)
        self.window = cmds.window(t='UV Set Name',tb=1,rtf=1)
        cmds.columnLayout(cal='center',adj=1)
        self.setNameFld = cmds.textFieldButtonGrp(
            l='Set Name', text='uvSet', bl='Del UV Set', bc=self.runCmd)
        cmds.showWindow(self.window)

    def runCmd(self):
        setName = cmds.textFieldButtonGrp(self.setNameFld, tx=1, q=1)
        #print('setName:{0}'.format(setName))
        curSel = cmds.ls(sl=1,fl=1)
        for sel in curSel:
            for uset in cmds.polyUVSet(sel,auv=1,q=1):
                if uset == setName:
                    cmds.polyUVSet(sel,uvSet=setName,d=1)
        cmds.deleteUI(self.window)
deleteUVset()._UI()
