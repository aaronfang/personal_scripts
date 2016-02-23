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
        else:
            cmds.confirmDialog(m="Please Select Shapes You Wish To Mirror")

    def selectBaseShape(self,*args):
        base_shape = cmds.ls(sl=True)[0]
        if len(base_shape)>0:
            for shape in self.cur_shapes:
                channels = []
                #Check "base_shape" and "shape" if channels are locked. If so unlock them.
                base_lock_list = cmds.listAttr(base_shape,locked=True)
                shape_lock_list = cmds.listAttr(shape,locked=True)
                if base_lock_list:
                    for x in base_lock_list:
                        channels.append("{1}.{0}".format(x,base_shape))
                elif shape_lock_list:
                    for x in shape_lock_list:
                        channels.append("{1}.{0}".format(x,shape))
                if len(channels)>0:
                    for channel in channels:
                        cmds.setAttr(channel,lock=False)
                self.CreateMirrorShape(base_shape,shape)
            
            if cmds.window("popupWin",exists=1):
                cmds.deleteUI("popupWin",window=1)
        else:
            cmds.confirmDialog(m="Please Select Base Shape Geo!")

    def CreateMirrorShape(self,base_shape,sculpt_shape):
        if base_shape and sculpt_shape:
            if "L_" in sculpt_shape and "left" not in sculpt_shape and "right" not in sculpt_shape:
                newShape="R_{0}".format(sculpt_shape.split('L_')[1])
                print sculpt_shape,newShape
            elif "R_" in sculpt_shape and "left" not in sculpt_shape and "right" not in sculpt_shape:
                newShape="L_{0}".format(sculpt_shape.split('R_')[1])
                print sculpt_shape,newShape
            elif "L_" in sculpt_shape and "left" in sculpt_shape and "right" not in sculpt_shape:
                newShape="R_{0}right{1}".format(sculpt_shape.split('L_')[1].split('left')[0],sculpt_shape.split('L_')[1].split('left')[1])
                print sculpt_shape,newShape
            elif "L_" in sculpt_shape and "left" not in sculpt_shape and "right" in sculpt_shape:
                newShape="R_{0}left{1}".format(sculpt_shape.split('L_')[1].split('right')[0],sculpt_shape.split('L_')[1].split('right')[1])
                print sculpt_shape,newShape
            elif "R_" in sculpt_shape and "left" in sculpt_shape and "right" not in sculpt_shape:
                newShape="L_{0}right{1}".format(sculpt_shape.split('R_')[1].split('left')[0],sculpt_shape.split('R_')[1].split('left')[1])
                print sculpt_shape,newShape
            elif "R_" in sculpt_shape and "left" not in sculpt_shape and "right" in sculpt_shape:
                newShape="L_{0}left{1}".format(sculpt_shape.split('R_')[1].split('right')[0],sculpt_shape.split('R_')[1].split('right')[1])
                print sculpt_shape,newShape
            elif "M_" in sculpt_shape and "left" not in sculpt_shape and "right" in sculpt_shape:
                newShape="{0}left{1}".format(sculpt_shape.split('right')[0],sculpt_shape.split('right')[1])
                print sculpt_shape,newShape
            elif "M_" in sculpt_shape and "left" in sculpt_shape and "right" not in sculpt_shape:
                newShape="{0}right{1}".format(sculpt_shape.split('left')[0],sculpt_shape.split('left')[1])
                print sculpt_shape,newShape
            else:
                newShape="Mirrored_{0}".format(sculpt_shape)
                print sculpt_shape,newShape
            
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
            new_shape = cmds.duplicate('baseWrap', name=newShape)
            if cmds.listRelatives(new_shape,p=True):
                cmds.parent(new_shape,w=True)
            
            #Clean up setup
            cmds.delete('baseWrap', 'baseScaleNeg')
            
mirrorSelectedShapes().main()
