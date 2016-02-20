import maya.cmds as cmds

class blendShapeEditor(object):

    def __init__(self):
        self.blendshape_node = blendshape_node = []
        self.target_nodes = target_nodes = []

    def prepareOrginialGeo(self,*args):
        sel = cmds.ls(sl=True)[0]
        if '_org' in sel:
            blendshape_base_geo = cmds.duplicate(sel,n="{0}_blendshape".format(sel.split('_org')[0]))
            layers = cmds.ls(type='displayLayer')
            if "org_geo_layer" not in layers:
                org_layer = cmds.createDisplayLayer(n="org_geo_layer",e=True)
                cmds.editDisplayLayerMembers(org_layer,sel,blendshape_base_geo,noRecurse=True)
                cmds.setAttr("{0}.displayType".format(org_layer),2)
            elif "org_geo_layer" in layers:
                cmds.editDisplayLayerMembers(org_layer,sel,noRecurse=True)
                cmds.setAttr("{0}.displayType".format(org_layer),2)
        else:
            cmds.confirmDialog(m="Please Select The Orginial Geo!")
        cmds.select(sel,blendshape_base_geo,r=True)

    def createBlendShape(self,*args):
        objs = cmds.ls(sl=True,fl=True)
        blendshape_node = cmds.blendShape(objs[0:-1],objs[-1],n="{0}_blendshape".format(objs[-1]))
        if len(blendshape_node)>0:
            for obj in objs[0:-1]:
                cmds.setAttr("{0}.visibility".format(obj),False)

    def _UI(self,*args):
        target_nodes = cmds.blendShape(blendshape_node[0],q=True,t=True)
        target_weights = cmds.blendShape(blendshape_node[0],q=True,w=True)
        if len(target_nodes)>0:
            w = 300
            if cmds.window('blendshapeWin',exists=True):cmds.deleteUI('blendshapeWin',window=True)
            cmds.window('blendshapeWin',t='BlendShape Editor',w=w,rtf=1,mxb=0,mnb=0,s=0)
            #cmds.columnLayout("mainColumn",p="blendshapeWin",columnAttach=('both', 2), rowSpacing=10, columnWidth=w)
            cmds.rowColumnLayout('mainRowColumn',p='blendshapeWin',numberOfColumns=3, columnWidth=[(1, 100), (2, 150), (3, 50)] )
            for i,tgt in enumerate(target_nodes):
                cmds.text(p='mainRowColumn',l=tgt)
                cmds.floatSlider("{0}FltSld".format(tgt),p='mainRowColumn',v=target_weights[i],max=1,min=0,cc=self.updateTargetValue)
                cmds.button(p='mainRowColumn',l='Edit')
            cmds.showWindow('blendshapeWin')

    def updateTargetValue(self,*args):
        for i,tgt in enumerate(target_nodes):
            last_value = cmds.blendShape(blendshape_node[0],q=True,w=True)
            cur_value = cmds.floatSlider("{0}FltSld".format(tgt),q=True,v=True)
            if cur_value != last_value:
                cmds.blendShape(blendshape_node[0],e=True,w=(i,cur_value))
        
blendShapeEditor()._UI()
