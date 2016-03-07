# UI
# if cmds.window("setAttrWin",exists=1):cmds.deleteUI("setAttrWin",window=1)
# w=450
# window=cmds.window("setAttrWin",t="BlendShape Tools",s=0,mb=1,rtf=1,mxb=0,mnb=0,w=w)

# Add coordinate attribute
objs = cmds.ls(sl=1,fl=1,type='transform')
name = "pivotCenter"
for obj in objs:
    if name in cmds.listAttr(obj):
        cfm_dlg = cmds.confirmDialog( title='Confirm', message='Duplicated Attribute!Do you want to delete it?', 
                           button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
        if cfm_dlg == 'Yes':
            cmds.deleteAttr("{0}.{1}".format(obj,name))
            # perform new attrs
            v1,v2,v3 = [0,0,0]
            cmds.addAttr(obj,ln=name,at='double3')
            for attr_name in ["{0}X".format(name),"{0}Y".format(name),"{0}Z".format(name)]:
                print attr_name
                cmds.addAttr(obj,ln=attr_name,at='double',p=name)
            cmds.setAttr("{0}.{1}".format(obj,name),v1,v2,v3,type='double3')
            for attr_name in ["{0}X".format(name),"{0}Y".format(name),"{0}Z".format(name)]:
                cmds.setAttr("{0}.{1}".format(obj,attr_name),e=True,k=True)

# Add single string attribute
objs = cmds.ls(sl=1,fl=1,type='transform')
name = "MDL"
for obj in objs:
    if name in cmds.listAttr(obj):
        cfm_dlg = cmds.confirmDialog( title='Confirm', message='Duplicated Attribute!Do you want to delete it?', 
                           button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
        if cfm_dlg == 'Yes':
            cmds.deleteAttr("{0}.{1}".format(obj,name))
            # perform new attrs
            string = "test string"
            cmds.addAttr(obj,ln=name,dt='string')
            cmds.setAttr("{0}.{1}".format(obj,name),string,type='string',e=True,k=True)

# Get pivot center
v1,v2,v3 = cmds.xform(obj,q=True,ws=True,piv=True)[0:3]
