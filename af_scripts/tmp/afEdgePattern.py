import maya.cmds as mc
import re
from types import *

def main():
    #get edge IDs
    curSel = mc.ls(sl=1,fl=1)
    edgeID = []
    for str in curSel:
       edgeID.append(int(re.split('[]]',(re.split('[[]',str)[1]))[0]))
    #print(edgeID)
    
    # check if loop
    edgeLoopGp = mc.polySelect(el=edgeID[0],q=1)
    if len(edgeLoopGp)>1:
        loopLst = []
        for edge in edgeLoopGp:
            edge = repr(edge)
            if edge.find(repr(edgeID[1]))==0:
                loopLst.append(edge)
        isEL = len(loopLst)
    else:
        isEL = 0
    
    # check if ring
    edgeRingGp = mc.polySelect(er=edgeID[0],q=1)
    if len(edgeRingGp)>1:
        RingLst = []
        for edge in edgeRingGp:
            edge = repr(edge)
            if edge.find(repr(edgeID[1]))==0:
                RingLst.append(edge)
        isER = len(RingLst)
    else:
        isER = 0     
    
    # check if border
    edgeBorderGp = mc.polySelect(eb=edgeID[0],q=1)
    if type(edgeBorderGp) is ListType:
        if len(edgeBorderGp)>1:
            BorderLst = []
            for edge in edgeBorderGp:
                edge = repr(edge)
                if edge.find(repr(edgeID[1]))==0:
                    BorderLst.append(edge)
            isBd = len(BorderLst)
        else:
            isBd = 0
    
    #do pattern
    if isEL==1:
        # edge loop pattern
        mc.polySelect(lpt=(edgeID[0],edgeID[1]))
    elif isER==1:
        #edge ring pattern
        mc.polySelect(rpt=(edgeID[0],edgeID[1]))
    elif isBd==1:
        #edge ring pattern
        mc.polySelect(bpt=(edgeID[0],edgeID[1]))
