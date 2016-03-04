def dupTransValue():
    objs = cmds.ls(sl=1,fl=1)
    source_obj = objs[0]
    target_obj = objs[1]
    for attr in ['tx','ty','tz','rx','ry','rz','sx','sy','sz']:
        new_attr = cmds.getAttr("{0}.{1}".format(target_obj,attr))
        cmds.setAttr("{0}.{1}".format(source_obj,attr),new_attr)
dupTransValue()
