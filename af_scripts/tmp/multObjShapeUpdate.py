import maya.cmds as cmds

def multObjShapeImport():
    files_to_import = cmds.fileDialog2(fileFilter =  '*.obj', dialogStyle = 2, caption = 'import multiple object files', fileMode = 4,okc="Import")
    for file_to_import in files_to_import:
        object_name  = file_to_import.split('/')[-1].split('.obj')[0]
        returnedNodes = cmds.file('%s' % file_to_import, i = True, type = "OBJ", rnn=True, ignoreVersion = True, options = "mo=0",  loadReferenceDepth  = "all"  )
        cmds.delete(cmds.ls(returnedNodes,type="objectSet"))
        geo = cmds.listRelatives(cmds.ls(returnedNodes,g=1)[0],p=1)
        cmds.rename( geo, object_name)

def multObjShapeUpdate():
    sel_objs = cmds.ls(sl=True,fl=True)
    if len(sel_objs)>0:
        files_to_import = cmds.fileDialog2(fileFilter =  '*.obj', dialogStyle = 2, caption = 'import multiple object files', fileMode = 4,okc="Import")
        if len(files_to_import) == len(sel_objs):
            object_names = [file_to_import.split('/')[-1].split('.obj')[0] for file_to_import in files_to_import]
            if len(sel_objs) == len([x for x in object_names if x in sel_objs]):
                for file_to_import in files_to_import:
                    object_name  = file_to_import.split('/')[-1].split('.obj')[0]
                    returnedNodes = cmds.file('%s' % file_to_import, i = True, type = "OBJ", rnn=True, ignoreVersion = True, options = "mo=0",  loadReferenceDepth  = "all"  )
                    cmds.delete(cmds.ls(returnedNodes,type="objectSet"))
                    geo = cmds.listRelatives(cmds.ls(returnedNodes,g=1)[0],p=1)
                    cmds.rename( geo, "newShape_{0}".format(object_name))
                new_shapes = [s for s in cmds.listRelatives(cmds.ls(g=1),p=1) if "newShape_" in s]
                cur_shapes = sel_objs
                for new in new_shapes:
                    for cur in cur_shapes:
                        if new.split("newShape_")[1] == cur:
                            blendshapeNd = cmds.blendShape(new,cur)[0]
                            cmds.setAttr("{0}.{1}".format(blendshapeNd,new),1)
                cmds.delete(cur_shapes,ch=True)
                cmds.delete(new_shapes)
                cmds.confirmDialog(m="---===All Shapes Updated!===---")
            else:
                cmds.confirmDialog(m="--==Not Matching The Name!==--")
        else:
            cmds.confirmDialog(m="--==Please Select The Same Number Of Objects!==--")
    else:
        cmds.confirmDialog(m="--==Please Select Something!==--")


multObjShapeUpdate()
