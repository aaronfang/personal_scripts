from pymel.core import *

tx = ls(sl=1, fl=1)

for i in tx:
    filePath = getAttr(i + ".fileTextureName")
    fullName = filePath.split('/')[-1]
    fileType = '.' + fullName.split('.')[-1]
    txName = fullName.rstrip(fileType)
    rename(i, txName)
