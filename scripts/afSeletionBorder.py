import pymel.core as pm

faceSel = pm.ls(sl=True,fl=True)
pm.mel.eval('ConvertSelectionToEdges')
allEd = pm.ls(sl=True,fl=True)
pm.select(faceSel,r=True)
pm.mel.eval('ConvertSelectionToContainedEdges')
insideEd = pm.ls(sl=True,fl=True)
pm.select(cl=True)
selBorderEd = []
for ed in allEd:
    if ed not in insideEd:
        selBorderEd.append(ed)
pm.select(selBorderEd,r=True)
