# DreamWorks Animation LLC Confidential Information.
# TM and (c) 2011 DreamWorks Animation LLC.  All Rights Reserved.
# Reproduction in whole or in part without prior written permission of a
# duly authorized representative is prohibited.



def mod_surfSortList(items):
    """Sort the given list of objects and reorder them in the maya scene.
    """
    mcmd = odwmaya.importMaya().cmds
    # make a shallow copy of items
    # 
    items = [i for i in items]

    # Sort items
    # 
    items.sort(cmp=dwacore.utils.sort.alphaNumericSort)
    
    for item in items:
        mcmd.reorder(item, back=True)

    for item in items:
        children = mcmd.listRelatives(item, f=1)
        if children:
            mod_surfSortList(children)
        
def mod_surfSort():
    """Sort the selected items according to name.
    """
    mcmd = odwmaya.importMaya().cmds
    selected = mcmd.ls(sl=True, l=True)
    mod_surfSortList(selected)
    
    


# TM and (c) 2011 DreamWorks Animation LLC.  All Rights Reserved.
# Reproduction in whole or in part without prior written permission of a
# duly authorized representative is prohibited.
