import pymel.core as pm
import re
import maya.mel as mel

### rename container 'HDRIs' file nodes to the textures name
ctns = []
for ctn in pm.ls(type='container',fl=True):
    if len(re.findall('HDRIs',str(ctn)))>0 and re.findall('HDRIs',str(ctn))[0]=='HDRIs':
        ctns.append(ctn)
if len(ctns)==1:
    pm.select(ctns[0],r=True)
    mel.eval('SelectContainerContents')
    hdrs = pm.ls(sl=True,fl=True)

    nameList = []
    
    for hdr in hdrs:
        texPath = pm.getAttr(hdr+'.fileTextureName')
        texName = re.split('/',texPath)[-1].split('.')[0]
        pm.rename(hdr,texName)
        nameList.append(hdr)
    print nameList
### End rename
