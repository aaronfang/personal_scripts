import maya.cmds as cmds

class mirrorSelectedShapes(object):
    def __init__(self):
        self.sculpt_shape = sculpt_shape = ""
        self.base_shape = base_shape = ""
        self.cur_shapes = []
        

    def main(self,*args):
        self.cur_shapes = cmds.ls(sl=True,fl=True)
        if len(self.cur_shapes)>0:
            if cmds.window("popupWin",exists=1):
                cmds.deleteUI("popupWin",window=1)
            cmds.window("popupWin",t="Select Base Shape",wh=(160,20),rtf=1,mnb=0,mxb=0,s=0)
            cmds.columnLayout()
            cmds.button(l="Now Select the \"Base Shape\".",c=self.selectBaseShape)
            cmds.showWindow("popupWin")


    def selectBaseShape(self,*args):
        base_shape = cmds.ls(sl=True)[0]
        if len(base_shape)>0:
            for shape in self.cur_shapes:
                self.CreateMirrorShape(base_shape,shape)
            if cmds.window("popupWin",exists=1):
                cmds.deleteUI("popupWin",window=1)
        else:
            cmds.confirmDialog(m="Please Select Base Shape Geo!")


    def CreateMirrorShape(self,base_shape,sculpt_shape):
        if "L_" in sculpt_shape and "left" not in sculpt_shape and "right" not in sculpt_shape:
            newShape="R_{0}".format(sculpt_shape.split('L_')[1])
        elif "R_" in sculpt_shape and "left" not in sculpt_shape and "right" not in sculpt_shape:
            newShape="L_{0}".format(sculpt_shape.split('L_')[1])
        elif "L_" in sculpt_shape and "left" in sculpt_shape and "right" not in sculpt_shape:
            newShape="R_{0}right{1}".format(sculpt_shape.split('L_')[1].split('left')[0],sculpt_shape.split('L_')[1].split('left')[1])
        elif "L_" in sculpt_shape and "left" not in sculpt_shape and "right" in sculpt_shape:
            newShape="R_{0}left{1}".format(sculpt_shape.split('L_')[1].split('right')[0],sculpt_shape.split('L_')[1].split('right')[1])
        elif "R_" in sculpt_shape and "left" in sculpt_shape and "right" not in sculpt_shape:
            newShape="L_{0}right{1}".format(sculpt_shape.split('R_')[1].split('left')[0],sculpt_shape.split('L_')[1].split('left')[1])
        elif "R_" in sculpt_shape and "left" not in sculpt_shape and "right" in sculpt_shape:
            newShape="L_{0}left{1}".format(sculpt_shape.split('R_')[1].split('right')[0],sculpt_shape.split('L_')[1].split('right')[1])
        else:
            newShape="Mirrored_{0}".format(sculpt_shape)

        #Create Wrap and Negative shape
        cmds.duplicate(base_shape, name="baseWrap")
        cmds.duplicate(base_shape, name="baseScaleNeg")
        
        #Flip Scale  
        cmds.setAttr("baseScaleNeg.scaleX", -1)

        #Blend Sculped shape to flipped shape
        cmds.blendShape(sculpt_shape, 'baseScaleNeg', name='TempBlend')
        
        #Create Wrap between wrap shape and Neg Shape
        cmds.select(cl=True)
        cmds.select('baseWrap')
        cmds.select('baseScaleNeg', add=True)
        cmds.CreateWrap()
        cmds.select(cl=True)
        
        cmds.setAttr("wrap1.exclusiveBind", 1)

        #Now turn on our Negated blendShpe
        cmds.setAttr("TempBlend."+sculpt_shape, 1)

        #Duplicate Wrapped shape for final result
        cmds.duplicate('baseWrap', name=newShape)
        
        #Clean up setup
        cmds.delete('baseWrap', 'baseScaleNeg')

mirrorSelectedShapes().main()
