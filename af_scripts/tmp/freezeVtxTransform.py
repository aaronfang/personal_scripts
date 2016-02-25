import pymel.core as pm


def freezeVtxTransformation():
    curSel = pm.ls(sl=1, fl=1)
    for sel in curSel:
        sel = sel.getShape()
        pm.polyMoveVertex(sel, ch=0)
        pm.select(d=True)


freezeVtxTransformation()
