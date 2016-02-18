import maya.cmds as cmds

class mirrorSelectedShapes(object):
    def __init__(self):
        self.sculpt_shape = ""
        self.base_shape = ""
        

    def main(self,*args):
        cur_shapes = cmds.ls(sl=True,fl=True)
        if len(cur_shapes)>0:
            cmds.window("popupWin",t="Select Base Shape",rtf=1,mnb=0,mxb=0,s=0)
            cmds.columnLayout()
            cmds.button(l="Now Select the \"Base Shape\".",bc=selectBaseShape)
            cmds.showWindow("popupWin")
            for shape in cur_shapes:
                print shape,self.base_shape


    def selectBaseShape(self,*args):
        self.base_shape = cmds.ls(sl=True)[0]
        if len(self.base_shape)>0:
            if cmds.window("popupWin",exists=1):
                cmds.deleteUI("popupWin",window=1)
        else:
            cmds.confirmDialog(m="Please Select Base Shape Geo!")


    def CreateMirrorShape(self.base_shape,self.sculpt_shape):
        if "L_" in self.sculpt_shape and "left" not in self.sculpt_shape and "right" not in self.sculpt_shape:
            newShape="R_{0}".format(self.sculpt_shape.split('L_')[1])
        elif "R_" in self.sculpt_shape and "left" not in self.sculpt_shape and "right" not in self.sculpt_shape:
            newShape="L_{0}".format(self.sculpt_shape.split('L_')[1])
        elif "L_" in self.sculpt_shape and "left" in self.sculpt_shape and "right" not in self.sculpt_shape:
            newShape="R_{0}right{1}".format(self.sculpt_shape.split('L_')[1].split('left')[0],self.sculpt_shape.split('L_')[1].split('left')[1])
        elif "L_" in self.sculpt_shape and "left" not in self.sculpt_shape and "right" in self.sculpt_shape:
            newShape="R_{0}left{1}".format(self.sculpt_shape.split('L_')[1].split('right')[0],self.sculpt_shape.split('L_')[1].split('right')[1])
        elif "R_" in self.sculpt_shape and "left" in self.sculpt_shape and "right" not in self.sculpt_shape:
            newShape="L_{0}right{1}".format(self.sculpt_shape.split('R_')[1].split('left')[0],self.sculpt_shape.split('L_')[1].split('left')[1])
        elif "R_" in self.sculpt_shape and "left" not in self.sculpt_shape and "right" in self.sculpt_shape:
            newShape="L_{0}left{1}".format(self.sculpt_shape.split('R_')[1].split('right')[0],self.sculpt_shape.split('L_')[1].split('right')[1])
        else:
            newShape="Mirrored_{0}".format(self.sculpt_shape)

        #Create Wrap and Negative shape
        cmds.duplicate(self.base_shape, name="baseWrap")
        cmds.duplicate(self.base_shape, name="baseScaleNeg")
        
        #Flip Scale  
        cmds.setAttr("baseScaleNeg.scaleX", -1)

        #Blend Sculped shape to flipped shape
        cmds.blendShape(self.sculpt_shape, 'baseScaleNeg', name='TempBlend')
        
        #Create Wrap between wrap shape and Neg Shape
        cmds.select(cl=True)
        cmds.select('baseWrap')
        cmds.select('baseScaleNeg', add=True)
        cmds.CreateWrap()
        cmds.select(cl=True)
        
        cmds.setAttr("wrap1.exclusiveBind", 1)

        #Now turn on our Negated blendShpe
        cmds.setAttr("TempBlend."+self.sculpt_shape, 1)

        #Duplicate Wrapped shape for final result
        cmds.duplicate('baseWrap', name=newShape)
        
        #Clean up setup
        cmds.delete('baseWrap', 'baseScaleNeg')
