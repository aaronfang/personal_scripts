# move to object

import pymel.core as pm


def move_to_object():
    get_sel = pm.ls(sl=1, fl=1)
    if len(get_sel) == 2:
        src = get_sel[1]
        target = get_sel[0]
        src_oc = pm.objectCenter(src)
        target_oc = pm.objectCenter(target)
        vector = (src_oc[0] - target_oc[0]), (src_oc[1] - target_oc[1]), (src_oc[2] - target_oc[2])
        pm.xform(target, t=vector, r=1)


move_to_object()
