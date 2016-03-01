"""
This tool is design for the modeler to layout their UVs in more efficient way.
- Line up UVs based on object level to 'U' or 'V' direction with a certain gap provided.
- Layout UVs based on object level to each UDIMs
- RoadKill Pro plugin functions
- store and select a list of objects
added:
    - scale by ratio
    - align in UDIMs both U and V
    - each UV shell rotate 180
need to add:
	- scale to last
	- scale by ratio (with group)
"""

import maya.cmds as cmds
import math


class LineUpUVs(object):
    def __init__(self):
        self.Sels = []
        pass

    def _UI(self):
        if cmds.window("lineUpWin", exists=1):
            cmds.deleteUI("lineUpWin", window=1)
        w = 180
        self.window = cmds.window("lineUpWin", t="AlignUVs", s=0, mb=1, rtf=1, wh=(w, 25),mxb=0,mnb=0)

        cmds.columnLayout("mainColumn", p="lineUpWin",
                          columnAttach=('both', 0.5),
                          rowSpacing=10,
                          columnWidth=w)
        cmds.rowLayout(p="mainColumn", w=w, h=25,
                       numberOfColumns=4,
                       columnWidth4=(55, 55, 30, 30),
                       adjustableColumn=1,
                       columnAlign=(1, 'right'),
                       columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0), (4, 'both', 0)])
        self.floatField = cmds.floatField("gapWValueField", v=0.003)
        self.floatField = cmds.floatField("gapHValueField", v=0.003)
        self.button = cmds.button(l="U", c=self.lineup_U)
        self.button = cmds.button(l="V", c=self.lineup_V)

        cmds.rowLayout(p="mainColumn", w=w, h=25,
                       numberOfColumns=3,
                       columnWidth3=(55, 55, 40),
                       adjustableColumn=3,
                       columnAlign=(1, 'right'),
                       columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)])
        self.button = cmds.button(l="U-UDIM", c=self.lineup_U_in_UDIM)
        self.button = cmds.button(l="V-UDIM", c=self.lineup_V_in_UDIM)
        self.button = cmds.button(l="UDIM", c=self.layoutUVsToUDIM)

        cmds.separator(p="mainColumn", style='in')
        cmds.rowLayout(p="mainColumn", w=w, h=25,
                       numberOfColumns=4,
                       columnWidth4=(30, 30, 30, 40),
                       adjustableColumn=1,
                       columnAlign=(1, 'right'),
                       columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0), (4, 'both', 0)])
        self.button = cmds.button(l="Scale2Src", c=self.RK_ScaleToSrc)
        self.button = cmds.button(l="G", c=self.RK_Geometric)
        self.button = cmds.button(l="O", c=self.RK_Organic)
        self.button = cmds.button(l="S", c=self.RK_Straighten)

        cmds.separator(p="mainColumn", style='in')
        cmds.rowLayout(p="mainColumn", w=w, h=25,
                       numberOfColumns=3,
                       columnWidth3=(10, 30, 80),
                       adjustableColumn=1,
                       columnAlign=(1, 'right'),
                       columnAttach=[(1, 'both', 5), (2, 'both', 0), (3, 'both', 5)])
        cmds.text("Pixel Ratio", al="left")
        cmds.intField("ratioFld", value=50)
        cmds.button(l="Rescale UVs", c=self.scaleUVRatio)

        cmds.separator(p="mainColumn", style='in')
        cmds.rowLayout(p="mainColumn", w=w, h=25,
                       numberOfColumns=3,
                       columnWidth3=(10, 30, 80),
                       adjustableColumn=1,
                       columnAlign=(1, 'right'),
                       columnAttach=[(1, 'both', 5), (2, 'both', 0), (3, 'both', 5)])
        cmds.button(l="Rotate 180", c=self.rotateEachShell)

        cmds.separator(p="mainColumn", style='in')
        # # cmds.separator(p="mainColumn", style='in')
        # cmds.button(p="mainColumn", l="Store Selection", c=self.storeSelToList)
        # cmds.textScrollList("selListTextScroll", p="mainColumn", numberOfRows=5, allowMultiSelection=True)
        # cmds.popupMenu("listPopUp", p="selListTextScroll")
        # cmds.menuItem(p="listPopUp", l="Select All In List", c=self.selectAllInList)
        # cmds.menuItem(p="listPopUp", l="Remove Selected From List", c=self.rmvSelFromList)
        # cmds.menuItem(p="listPopUp", l="Remove All From List", c=self.rmvAllFromList)
        #
        # cmds.button(p="mainColumn", l="Select", c=self.selectHighlightedInList)

        cmds.showWindow(self.window)

    def layoutUVsToUDIM(self, *args):
        sels = cmds.ls(sl=1)
        for i, x in enumerate(sels):
            x = x.getShape()
            cmds.select('{0}.map[:]'.format(x), r=1)
            cmds.polyEditUV(u=i % 10, v=int(math.floor(i / 10)))
        cmds.select(sels, r=1)

    def lineup_U(self,*args):
        sels = cmds.ls(os=1)
        gap_w = cmds.floatField("gapWValueField", q=True, v=True)
        initGap = 0.003

        for i, x in enumerate(sels):
            cmds.select('{0}.map[:]'.format(x), r=1)

            if i == 0:
                # move to the init place
                cmds.polyEditUV(u=-cmds.polyEvaluate(x, b2=1)[0][0] + initGap, v=-cmds.polyEvaluate(x, b2=1)[1][0] + initGap)

            elif i >= 1:
                # get the U size of the last shell
                w_last = cmds.polyEvaluate(sels[i-1], b2=1)[0][1]-cmds.polyEvaluate(sels[i-1], b2=1)[0][0]
                # calc the distance to the last shell
                dist_u = cmds.polyEvaluate(x, b2=1)[0][0]-cmds.polyEvaluate(sels[i-1], b2=1)[0][0]
                dist_v = cmds.polyEvaluate(x, b2=1)[1][0]-cmds.polyEvaluate(sels[i-1], b2=1)[1][0]
                # move current shell to the last shell
                cmds.polyEditUV(u=-dist_u+w_last+gap_w, v=-dist_v)
        cmds.select(sels,r=1)

    def lineup_U_in_UDIM(self,*args):
        sels = cmds.ls(os=1)
        gap_w = cmds.floatField("gapWValueField", q=True, v=True)
        gap_h = cmds.floatField("gapHValueField", q=True, v=True)
        initGap = 0.003
        UDIM_limit = 10
        fst_in_UDIM = 0

        for i, x in enumerate(sels):
            cmds.select('{0}.map[:]'.format(x), r=1)

            if i == 0:
                # move to the init place
                cmds.polyEditUV(u=-cmds.polyEvaluate(x, b2=1)[0][0] + initGap, v=-cmds.polyEvaluate(x, b2=1)[1][0] + initGap)

            elif i >= 1:
                # get the U size of the last shell
                w_last = cmds.polyEvaluate(sels[i-1], b2=1)[0][1]-cmds.polyEvaluate(sels[i-1], b2=1)[0][0]
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
                elif int((math.floor(cmds.polyEvaluate(x, b2=1)[0][1])+1)+(math.floor(cmds.polyEvaluate(x, b2=1)[1][1])*10))-UDIM_last==10:
                    fst_in_UDIM = i
                    new2_u = -(cmds.polyEvaluate(x, b2=1)[0][0]-initGap)+(int((math.floor(cmds.polyEvaluate(x, b2=1)[0][1])+1)+(math.floor(cmds.polyEvaluate(x, b2=1)[1][1])*10))-UDIM_limit)
                    new2_v = -cmds.polyEvaluate(x, b2=1)[1][0] + initGap
                    cmds.polyEditUV(u=new2_u, v=new2_v)
        cmds.select(sels,r=1)

    def lineup_V(self,*args):
        sels = cmds.ls(os=1)
        gap_h = cmds.floatField("gapHValueField", q=True, v=True)
        initGap = 0.003

        for i, x in enumerate(sels):
            cmds.select('{0}.map[:]'.format(x), r=1)

            if i == 0:
                # move to the init place
                cmds.polyEditUV(u=-cmds.polyEvaluate(x, b2=1)[0][0] + initGap, v=-cmds.polyEvaluate(x, b2=1)[1][0] + initGap)

            elif i >= 1:
                # get the size of the last shell
                h_last = cmds.polyEvaluate(sels[i-1], b2=1)[1][1]-cmds.polyEvaluate(sels[i-1], b2=1)[1][0]
                # calc the distance to the last shell
                dist_u = cmds.polyEvaluate(x, b2=1)[0][0]-cmds.polyEvaluate(sels[i-1], b2=1)[0][0]
                dist_v = cmds.polyEvaluate(x, b2=1)[1][0]-cmds.polyEvaluate(sels[i-1], b2=1)[1][0]
                # move current shell to the last shell
                cmds.polyEditUV(u=-dist_u, v=-dist_v+h_last+gap_h)
        cmds.select(sels,r=1)

    def lineup_V_in_UDIM(self,*args):
        sels = cmds.ls(os=1)
        gap_w = cmds.floatField("gapWValueField", q=True, v=True)
        gap_h = cmds.floatField("gapHValueField", q=True, v=True)
        initGap = 0.003
        fst_in_UDIM = 0

        for i, x in enumerate(sels):
            cmds.select('{0}.map[:]'.format(x), r=1)

            if i == 0:
                # move to the init place
                cmds.polyEditUV(u=-cmds.polyEvaluate(x, b2=1)[0][0] + initGap, v=-cmds.polyEvaluate(x, b2=1)[1][0] + initGap)

            elif i >= 1:
                # get the size of the last shell
                w_last = cmds.polyEvaluate(sels[i-1], b2=1)[0][1]-cmds.polyEvaluate(sels[i-1], b2=1)[0][0]
                h_last = cmds.polyEvaluate(sels[i-1], b2=1)[1][1]-cmds.polyEvaluate(sels[i-1], b2=1)[1][0]
                # calc the distance to the last shell
                dist_u = cmds.polyEvaluate(x, b2=1)[0][0]-cmds.polyEvaluate(sels[i-1], b2=1)[0][0]
                dist_v = cmds.polyEvaluate(x, b2=1)[1][0]-cmds.polyEvaluate(sels[i-1], b2=1)[1][0]
                # move current shell to the last shell
                cmds.polyEditUV(u=-dist_u, v=-dist_v+h_last+gap_h)
                # get the UDIM ID of the current shell and the last shell
                UDIM = int((math.floor(cmds.polyEvaluate(x, b2=1)[0][1])+1)+(math.floor(cmds.polyEvaluate(x, b2=1)[1][1])*10))
                UDIM_last = int((math.floor(cmds.polyEvaluate(sels[i-1], b2=1)[0][1])+1)+(math.floor(cmds.polyEvaluate(sels[i-1], b2=1)[1][1])*10))
                # if shell V is out of UDIM
                if int((math.floor(cmds.polyEvaluate(x, b2=1)[0][1])+1)+(math.floor(cmds.polyEvaluate(x, b2=1)[1][1])*10))-UDIM_last==10:
                    new_u = -(cmds.polyEvaluate(x, b2=1)[0][0]-cmds.polyEvaluate(sels[fst_in_UDIM:i], b2=1)[0][1])+gap_w
                    new_v = -(cmds.polyEvaluate(x, b2=1)[1][0]-initGap)#+int(math.floor((UDIM-11) / 10))
                    cmds.polyEditUV(u=new_u, v=new_v)
                    if int((math.floor(cmds.polyEvaluate(x, b2=1)[0][1])+1)+(math.floor(cmds.polyEvaluate(x, b2=1)[1][1])*10))-UDIM_last==1:
                        new_u = -(cmds.polyEvaluate(x, b2=1)[0][0]-initGap)+(int((math.floor(cmds.polyEvaluate(x, b2=1)[0][1])+1)+(math.floor(cmds.polyEvaluate(x, b2=1)[1][1])*10))-1)
                        new_v = -(cmds.polyEvaluate(x, b2=1)[1][0]-initGap)#+int(math.floor((UDIM-11) / 10))
                        cmds.polyEditUV(u=new_u, v=new_v)
                    # elif cmds.polyEvaluate(x, b2=1)[0][0] > 10:
                    #     new_u = -cmds.polyEvaluate(x, b2=1)[0][0]+initGap
                    #     new_v = cmds.polyEvaluate(x, b2=1)[1][0]+1
                    #     cmds.polyEditUV(u=new_u, v=new_v)
                elif int((math.floor(cmds.polyEvaluate(x, b2=1)[0][1])+1)+(math.floor(cmds.polyEvaluate(x, b2=1)[1][1])*10))-UDIM_last==1:
                    new_u = -(cmds.polyEvaluate(x, b2=1)[0][0]-cmds.polyEvaluate(sels[fst_in_UDIM:i], b2=1)[0][1])+gap_w
                    new_v = -(cmds.polyEvaluate(x, b2=1)[1][0]-initGap)+int(math.floor((UDIM-11) / 10))
                    cmds.polyEditUV(u=new_u, v=new_v)
        cmds.select(sels,r=1)

    def RK_Geometric(self, *args):
        if not cmds.pluginInfo("Roadkill", q=1, l=1):
            cmds.loadPlugin("Roadkill")
        cmds.mel.eval("RoadkillProGeometric")

    def RK_Organic(self, *args):
        if not cmds.pluginInfo("Roadkill", q=1, l=1):
            cmds.loadPlugin("Roadkill")
        cmds.mel.eval("RoadkillProOrganic")

    def RK_Straighten(self, *args):
        if not cmds.pluginInfo("Roadkill", q=1, l=1):
            cmds.loadPlugin("Roadkill")
        cmds.mel.eval("RoadkillProStraighten")

    def RK_ScaleToSrc(self, *args):
        if not cmds.pluginInfo("Roadkill", q=1, l=1):
            cmds.loadPlugin("Roadkill")
        cmds.mel.eval("RoadkillProScaleToSource")

    def selMesh(self, *args):
        getSel = cmds.ls(sl=1, fl=1)
        listItems = cmds.textScrollList("selListTextScroll", q=1, ai=1)
        curSelInList = cmds.textScrollList("selListTextScroll", q=1, si=1)
        if len(getSel) == 0:
            if len(curSelInList) != 0:
                cmds.select(curSelInList, r=1)
            else:
                cmds.select(listItems, r=1)
        elif len(getSel) >= 1:
            self.Sels = getSel
            if len(listItems) == 0:
                cmds.textScrollList("selListTextScroll", e=1, append=self.Sels)
            elif len(listItems) >= 1:
                if sel not in listItems:
                    cmds.textScrollList("selListTextScroll", e=1, append=sel)

    def storeSelToList(self, *args):
        getSel = cmds.ls(sl=1, fl=1)
        listItems = cmds.textScrollList("selListTextScroll", q=1, ai=1)
        if len(getSel) >= 1:
            if len(listItems) == 0:
                cmds.textScrollList("selListTextScroll", e=1, append=getSel)
            elif len(listItems) >= 1:
                for sel in getSel:
                    if sel not in listItems:
                        cmds.textScrollList("selListTextScroll", e=1, append=sel)

    def rmvSelFromList(self, *args):
        curSelInList = cmds.textScrollList("selListTextScroll", q=1, si=1)
        cmds.textScrollList("selListTextScroll", e=1, ri=curSelInList)

    def rmvAllFromList(self, *args):
        cmds.textScrollList("selListTextScroll", e=1, ra=1)

    def selectHighlightedInList(self, *args):
        curSelInList = cmds.textScrollList("selListTextScroll", q=1, si=1)
        listItems = cmds.textScrollList("selListTextScroll", q=1, ai=1)
        if len(curSelInList) > 0:
            cmds.select(curSelInList, r=1)
        elif len(curSelInList) == 0:
            cmds.select(listItems, r=1)

    def selectAllInList(self, *args):
        listItems = cmds.textScrollList("selListTextScroll", q=1, ai=1)
        cmds.textScrollList("selListTextScroll", e=1, si=listItems)

    def scaleUVRatio(self, *args):
        res = 1024
        mult = 1
        mult = (mult * (8192 / res)) / 8
        densityField = cmds.intField("ratioFld", q=1, v=1)
        unfold = 0.0009765625 * densityField
        ratioField = unfold * mult
        cmds.unfold(i=0, us=True, s=ratioField)

    def rotateEachShell(self,*args):
        sels = cmds.ls(sl=1)
        for i, x in enumerate(sels):
            x = x.getShape()
            cmds.select('{0}.map[:]'.format(x), r=1)
            cmds.mel.eval("polyRotateUVs 180")
            cmds.select(sels, r=1)

LineUpUVs()._UI()
