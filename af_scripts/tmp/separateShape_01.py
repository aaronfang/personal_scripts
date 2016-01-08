#from sgtkutils.util import sgfunc
#reload(sgfunc)
import maya.cmds as cmds
#cmds.duplicate(cmds.ls(sl = True), ilf = True)
class SeparateShape(object):
    
    def __init__(self):
        
        #self.sgutil = sgfunc.Sgtkutil()
        self.asset = os.getenv('ASSET')
        
    def getAllShapes(self):
        
        assetTopNode = None
        
        allTopNodes = cmds.ls(assemblies = True)
        for topnode in allTopNodes:
            if(topnode == self.asset):
                print topnode
                assetTopNode = topnode
                
        if(assetTopNode == None):
            print("Can not find asset in all top trasform node!")
            return False
            
        allFirst = cmds.listRelatives(assetTopNode, c = True, f = True)
        for first in allFirst:
            print first
            if(len(cmds.listRelatives(first, ad = True)) > 1):
                
                oldMatrix = cmds.xform(first, q = True, ws = True, m = True)
                print oldMatrix
                allSecond = cmds.listRelatives(first, ad = True, f = True)
                for second in allSecond:
                    type = cmds.objectType(second)
                    if(type == "mesh"):
                        print second
                        shortName = second.split("|")[-1]
                        print shortName
                        newTransform = cmds.createNode("transform", n = shortName)
                        #cmds.setAttr(newTransform + ".xformMatrix", oldMatrix, type = "matrix")
                        newChild = cmds.rename(second, shortName + "Shape")
                        
                        newTransform = cmds.parent(newTransform, first, r = True)
                        print newTransform
                        cmds.parent(newChild, newTransform, r = True, s = True)
               
    def doMain(self):
        
        self.getAllShapes()
        
c = SeparateShape()
c.doMain()
