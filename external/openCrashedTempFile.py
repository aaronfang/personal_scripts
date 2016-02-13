from pymel.core import *
import maya.cmds as mc
import os,glob

class FindFileError(Exception):pass

# find the latest ma
temp_dir = os.environ.get('temp')
latest_ma = str()
latest_time = long(0)
for f in glob.glob(temp_dir+r'\*.ma'):
    f_t = long(os.stat(f).st_ctime)
    if latest_time < f_t:
        latest_time,latest_ma = f_t,f
if latest_time == 0:
    raise FindFileError
    
# open
ret = confirmDialog(title = 'Sure?',
    message = 'Are you sure to close current scene and open\n< '+latest_ma.split('\\')[-1]+" >?\nIf file is unsaved then your change would get lost.", 
    icn = 'question',
    button=['Yes','No'],defaultButton='Yes', cancelButton='No', dismissString='No' 
    )
    
if ret==u'Yes':
    mc.file(latest_ma,open=True,f=True)
