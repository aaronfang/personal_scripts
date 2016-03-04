# select geos have locked/hidden attrs, run the following code.
get_sel = cmds.ls(sl=True,fl=True)
for sel in get_sel:
    locked_attrs = cmds.listAttr(sel,locked=True)
    if locked_attrs and len(locked_attrs)>0:
        for attr in locked_attrs:
            cmds.setAttr("{0}.{1}".format(sel,attr),lock=False)
    for attr in ['tx','ty','tz','rx','ry','rz','sx','sy','sz','visibility']:
        iskeyable = cmds.getAttr("{0}.{1}".format(sel,attr),k=True)
        if not iskeyable:
            cmds.setAttr("{0}.{1}".format(sel,attr),k=True)
