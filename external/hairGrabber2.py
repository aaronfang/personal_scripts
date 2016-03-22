'''
Hair Grabber 2.87 by Alex Sizov
------------------------------
A tool for batch selection and manipulation of hair cards on characters or other poly plane assets. 
Gives the ability to select roots tips middles and other selection options for multiple hair card objects. 
Reconstructs proper orientation for hair cards that have lost their transforms. Fill the space between hair cards with more cards procedually. 
Randomize translation and rotation on cards and snap them to another object.
Helps with batch unfolding and keeping the UVs square, as well as transfering UVs from haircap to hairs.


The tool uses UVs to figure out the orientation of the card to determine the roots and the tips. a UV set must be loaded in to the tool for it to work properly.
current version still uses pymel for everything.

future plans might include:
*general unification and cleanup of the code
*rewriting the main processing parts to maya API2 for speed increase
*updatimg the logic of the fill button to follow a similar vector direction of cards to avoid matrix artefacts
*attempt an alternative to blendshapes by storing roots mids and tips with their local matricies and applying these to duplicated hairs
*attempt an alternate to tip finding method using neighbours on boundry and vert to check the angle in relation to each other.
small enough angle = tip. use UVs to split top from bottom
*make script more modular.
*store matrix for roots mids and tips to help with random translate and rotate

requests complaints and presents and other such communications can be sent to sizovalex@yahoo.com

cheers!
'''
import pymel.core as pm
import random
class HairGrabberUI(object):
    
    def __init__( self ):
        
        if pm.window('Hair Grabber 2', exists = True):
            pm.deleteUI('Hair Grabber 2')
        
        self.makeUi()
    
    def makeUi(self):
        ############################
        self.win = pm.window('Hair Grabber 2', title='Hair Grabber 2')
        with self.win:
            self.col = pm.columnLayout()
            with self.col:
                self.row1 = pm.rowLayout(nc=7)
                with self.row1:
                    self.tipBtn = pm.button(label="tip", width=70, c= lambda x: self.selectBatch(self.tip),
                        ann = 'grabs the tips of a plane or multiple planes' )
                    self.rootBtn = pm.button(label="root", width=70, c= lambda x: self.selectBatch(self.root),
                        ann = 'grabs the roots of a plane or multiple planes' )
                    self.middleBtn = pm.button(label="middle", width=70,c= lambda x: self.selectBatch(self.middle) ,
                        ann = 'grabs the middle edgeloop of a plane or multiple plains. if the mid checkbox is selected,'\
                            'the randT slider above it will control the positioning of the edgeloop in relation to the edge or tip'    )
                    self.middle2Btn = pm.button(label="length", width=60, c = lambda x: self.selectBatch(self.middle2),
                        ann = 'grabs the length edgeloops of the plane or planes.' )
                    self.transformBtn = pm.button(label="Transform", width=60, c= lambda x: self. transform(),
                        ann = 'selects the transform node if any other component like verts or faces is selected' )
                    self.edgeFlowBtn = pm.button(label="edgeFlow", width=60, c= lambda x: self.edgeFlow(),
                        ann = 'goes over edgeloops and performs edgeflow on each. it returns a smoother transition in case the geo is jagged'\
                            'if the checkbox to the right is selected it also iterates over the length edgeloops ' )
                    self.lenCheckBox = pm.checkBox(label = '||', value = False , ann = 'length edgeloops activated')
                self.row2 = pm.rowLayout(nc=7)
                with self.row2:
                    self.pivotBtn = pm.button(label="pivot", width=70, c = lambda x: self.pivot(), 
                        ann = 'sets the pivot for each selected geo plane to its first row of faces and alligns to its normal' )
                    self.snapPivotBtn = pm.button(label='snapPivot', width=70, c=lambda x: self.snapPivot(),
                        ann = 'if geo is fed in to the haircap field it will snap selected transforms to the closest point on that geo.' )
                    self.snapBtn = pm.button(label="snap", width=70, c=lambda x: self.snap() ,
                        ann = 'if geo is fed in to the haircap field it snaps the verts of whatever geo is selected to it.'\
                            ' if specific verts selected it will only snap them')
                    self.fillBtn = pm.button(label="fill", width=70, c=lambda x:  self.fill(  self.amountField.getValue()+1  ),
                        ann = 'duplicates the selected geo. if one is selected itll fill the surroundings of that geo.'\
                            'if multiple pices are selected itll iterate from the first one to the next and fill the in betweens'
                            'you can controll the offset and random rotation with both sliders, and input the amount of'\
                            'copies using the amount field to its right' )
                    self.amountField = pm.intField( 'amount', w = 40, annotation = 'times' , value = 1 ,minValue=1 , maxValue=30)
                    self.transferCheckBox = pm.checkBox(label = 'uv', value = False ,
                        ann = 'transfers the UVs from map1 of the haircap to the newly created objects, or if active same function works for transfer button')
                    self.transferBtn = pm.button(label="transfer", width=63, c=lambda x: self.transfer(),
                        ann = 'transfers uvs for current UVsets to selection from last selected, or '\
                            'transfers the UVs from map1 of the haircap to the selected objects if uv checkBox is on ' )
                self.row3 = pm.rowLayout(nc=5)
                with self.row3:
                    self.randSliderT = pm.floatSlider( horizontal = True,width = 168, min=0, max=10, value=0, 
                        cc = lambda x:self.middleCond(),
                        ann = 'controls the random translate values and affected by the 3 axes under it. if mid is on'\
                            'the field will select the edgeloop of selected geo accordint to the placement on the slider'\
                            'as well as the percentage of the random transform select button' )
                    self.Text3 = pm.button(label="randT", width=44, c=lambda x:  self.randomize(pm.selected(), transRot = 0 ),
                        ann = ' randomly translates values and affected by the 3 axes under it' )
                    self.randSliderR = pm.intSlider( horizontal = True,width = 168, min=0, max=90, value=0, step=1 ,
                        ann = 'controls the random rotation values and affected by the 3 axes under it. set to max value of 90')
                    self.Text4 = pm.button(label="randR", width=44, c=lambda x:  self.randomize(pm.selected(), transRot = 1 ),
                        ann = ' randomly rotates values and affected by the 3 axes under it' )
                self.row4 = pm.rowLayout(nc=9)
                with self.row4:
                    self.midCtrlCheckBox = pm.checkBox(label = 'mid', value = False )
                    self.TXCheckBox = pm.checkBox(label = ' TX ', value = True )
                    self.TYCheckBox = pm.checkBox(label = ' TY ', value = True )
                    self.TZCheckBox = pm.checkBox(label = ' TZ ', value = True )
                    self.RandTransBtn = pm.button(label="random transform select", 
                        width=130, c=lambda x:  self.randomTransformSel(pm.selected()),
                        ann = 'uses the left transform slider to select a percent of previously selected geo'  )
                    self.RXCheckBox = pm.checkBox(label = ' RX ', value = True )
                    self.RYCheckBox = pm.checkBox(label = ' RY ', value = True )
                    self.RZCheckBox = pm.checkBox(label = ' RZ ', value = True )
                self.row5 = pm.rowLayout(nc=8)
                with self.row5:
                    self.Text1 = pm.text("UVset")
                    self.UvSetSearchName = pm.textField('name of UV set', w = 93, it = "Alpha",
                        ann = 'uses UVs that are upright to determine the roots and tips of a geo plane. a separate UVset can be created'\
                            'and loaded to this field.')
                    self.grabUVBtn = pm.button(label="grab", width=30, c=lambda x:  self.grabUV() ,
                        ann = 'gets the current active UVset of selected object')
                    self.fixUVBtn = pm.button(label="unfold inner", width=73, c=lambda x:  self.UVFix()  ,
                        ann = 'attempts to fix UVs if in the modelling process they get mangled. when the checkbox to the right'\
                            'is activated it also flattens the length boarders to the average of tips and roots to give rectangular result.')
                    self.squareCheckBox = pm.checkBox(label = '[]', value = True,
                        ann = 'flattens the length boarders to the average of tips and roots to give rectangular result to UVs' )
                    self.Text2 = pm.text("haircap")
                    self.capName = pm.textField('name of haircap', w = 93, it = "geo_head",
                        ann = 'write down or select geo and use grab button to the right to feed it to the script.' )
                    self.grabCapBtn = pm.button(label="grab", width=30, c=lambda x:  self.grabCap() ,
                        ann = 'grabs the name of active geo' )
                self.win.show()
#############################
#############################functions for getting active uv set and haircap object's name
    def grabUV(self):
        uv = pm.polyUVSet(cuv = 1, q = 1)[0]
        self.UvSetSearchName.setText(uv)
        
    def grabCap(self):
        name = pm.ls(sl = 1)[0]
        self.capName.setText(name)
        
############################general processing. find flat UVs and tips of geo
    def findFlatUvSet(self, s):
        sub = self.UvSetSearchName.getText().lower()
        flatUvSet = [n for n in pm.polyUVSet(s, q = True, allUVSets = True) if sub in n.lower()]
        if len(flatUvSet)>=1:
            return flatUvSet[0]
        else:pm.error('no matching UV set')
    
    def findTips(self, s, flatUvSet):
        tips, tipsUV, pair1, pair2 = [],[],[],[]
        for selVert in s.vtx:
            if selVert.isOnBoundary() and len(selVert.connectedVertices()) < 3:
                tips.append(selVert)
        for t in tips:
            tipsUV.append(t.getUV(str(flatUvSet)))
        tipUvAvg = [sum(tipsUV[0])/len(tipsUV[0]), sum(tipsUV[1])/len(tipsUV[1])]
        for t in tips:
            if t.getUV( str(flatUvSet) )[1]>  tipUvAvg[1] :
                pair1.append(t)
            else: pair2.append(t)
        pair1.sort(key=lambda item: (item.getUV( str(flatUvSet) )[0], item)    )
        pair2.sort(key=lambda item: (item.getUV( str(flatUvSet) )[0], item)    )
        return pair1, pair2
    
#####################################grab different parts of geo    
    def selectBatch(self, selTarget):
        pm.select(pm.ls(o=1, sl=1))
        selected = pm.ls(sl = 1)
        pm.select(cl = 1)
        result = []
        for s in selected:
            result.append(selTarget(s)    )
        pm.select(result)
            
        
    def tip(self, s):
        #######selects the tip edges of the geo
        flatUvSet = self.findFlatUvSet(s)
        pair1, pair2 = self.findTips(s, flatUvSet)
        tip = []
        if len(pair2) > 1:
            for x in range(len(pair2)-1):
                tip.append(    pm.polySelect(s, shortestEdgePathUV = (pair2[x].getUVIndices(str(flatUvSet))[0], 
                    pair2[x+1].getUVIndices(str(flatUvSet))[0]), ass = 1)    )
            tip = [val for sublist in tip for val in sublist]
        else:
            tip = pair2[0]
        return tip
    
    def root(self,s):
        #######selects the root edges of the geo
        flatUvSet = self.findFlatUvSet(s)
        pair1, pair2 = self.findTips(s, flatUvSet)
        root = []
        if len(pair1) > 1:
            for x in range(len(pair1)-1):
                root.append(    pm.polySelect(s, shortestEdgePathUV = (pair1[x].getUVIndices(str(flatUvSet))[0], 
                    pair1[x+1].getUVIndices(str(flatUvSet))[0]), ass = 1)    )
            root = [val for sublist in root for val in sublist]
        else:
            root = pair1[0]
        return root
    
    def middleCond(self):
        if self.midCtrlCheckBox.getValue() == 1:
            self.selectBatch(self.middle)
    
    def middle(self,s):
        
        if self.midCtrlCheckBox.getValue() == 1:
            number = self.randSliderT.getValue()/10
        else: number = 0.5
        #use input field data to determine flat uv set
        flatUvSet = self.findFlatUvSet(s)
        #get tips of geo and split to top and bottom pairs
        pair1, pair2 = self.findTips(s, flatUvSet)
        #select edges going the length on the cards and list as vertices
        pm.polyUVSet(s, currentUVSet =1, uvSet=flatUvSet)###not sure that I need it
        side1Edge = pm.polySelect(s, ass = 1, shortestEdgePathUV = (pair1[0].getUVIndices(str(flatUvSet))[0], pair2[0].getUVIndices(str(flatUvSet))[0]))
        side1 = pm.ls(pm.polyListComponentConversion(side1Edge, fe =1, tv =1), fl = 1)
        side2Edge = pm.polySelect(s, ass = 1, shortestEdgePathUV = (pair1[1].getUVIndices(str(flatUvSet))[0], pair2[1].getUVIndices(str(flatUvSet))[0]))
        side2 = pm.ls(pm.polyListComponentConversion(side2Edge, fe =1, tv =1), fl = 1)
        #select bottom verts and walk(traverse) to the middle of the geo on both sides
        mid1 = pm.ls(self.traverse(start = pair1[0], listToWalk  = side1, multiplyBy = number ))
        mid2 = pm.ls(self.traverse(start = pair1[1], listToWalk  = side2, multiplyBy = number ))
        #select shortest path between the 2 middle points and add to the middleL list
        MidLine = pm.polySelect(s, ass = 1, shortestEdgePathUV = (mid1[0].getUVIndices(str(flatUvSet))[0], mid2[0].getUVIndices(str(flatUvSet))[0]))
        pm.select(cl = 1)
        return MidLine
    
    
    def middle2(self, s):
        middleL = []
        #use input field data to determine flat uv set
        flatUvSet = self.findFlatUvSet(s)
        #get tips of geo and split to top and bottom pairs
        pair1, pair2 = self.findTips(s, flatUvSet)
        #select edges going the length on the cards and list as vertices
        pm.polyUVSet(s, currentUVSet =1, uvSet=flatUvSet)
        side1Edge = pm.polySelect(s, ass = 1, shortestEdgePathUV = (pair1[0].getUVIndices(str(flatUvSet))[0], pair1[1].getUVIndices(str(flatUvSet))[0]))
        side1 = pm.ls(pm.polyListComponentConversion(side1Edge, fe =1, tv =1), fl = 1)
        if len(side1) > 2:
            side2Edge = pm.polySelect(s, ass = 1, shortestEdgePathUV = (pair2[0].getUVIndices(str(flatUvSet))[0], pair2[1].getUVIndices(str(flatUvSet))[0]))
            side2 = pm.ls(pm.polyListComponentConversion(side2Edge, fe =1, tv =1), fl = 1)
            #select bottom verts and walk(traverse) to the middle of the geo on both sides
            mid1 = pm.ls(self.traverse(start = pair1[0], listToWalk  = side1, multiplyBy = 0.5 ))
            mid2 = pm.ls(self.traverse(start = pair2[0], listToWalk  = side2, multiplyBy = 0.5 ))
            #select shortest path between the 2 middle points and add to the middleL list
            MidLine = pm.polySelect(s, ass = 1, shortestEdgePathUV = (mid1[0].getUVIndices(str(flatUvSet))[0], mid2[0].getUVIndices(str(flatUvSet))[0]))
            middleL.append(MidLine)
            pm.select(cl = 1)
            if len(side1) % 2 == 0:
                mid3 = pm.ls(self.traverse(start = pair1[-1], listToWalk  = side1, multiplyBy = 0.5 ))
                mid4 = pm.ls(self.traverse(start = pair2[-1], listToWalk  = side2, multiplyBy = 0.5 ))
                MidLine2 = pm.polySelect(s, ass = 1, shortestEdgePathUV = (mid3[0].getUVIndices(str(flatUvSet))[0], mid4[0].getUVIndices(str(flatUvSet))[0]))
                middleL.append(MidLine2)
                pm.select(cl = 1)
        return pm.ls(	middleL,    fl = True)


###################extra functions: edgeflow, snap selection, snap pivot, select Transform, transfer attributes
    
    def edgeFlow(self):
        oldSel = pm.ls(sl = 1)
        pm.select(pm.ls(o=1, sl=1))
        selected = pm.ls(sl = 1)
        pm.delete(selected, constructionHistory = 1)
        pm.select(cl = 1)
        for s in selected:
            rootEdges = pm.ls(    self.root(s)    , fl = 1)
            tipEdges =  pm.ls(    self.tip(s)    , fl = 1)
            ############length edgeloops of the card
            myEdges = pm.ls(pm.polySelect(s, ebp = [    rootEdges[0].index(), tipEdges[0].index()    ],ass = True ), fl = 1)
            side1Edges = [x for x in myEdges if x not in rootEdges and x not in tipEdges]
            borderEdges = [x for x in pm.ls(s.e, fl = 1) if x.isOnBoundary()]
            pm.select(tipEdges)
            for x in range(len(side1Edges)*2):
                if x != borderEdges and x!= rootEdges and x!= tipEdges:
                    pm.polyEditEdgeFlow(adjustEdgeFlow=1, constructionHistory=0)
                    pm.pickWalk(type = 'edgeloop', direction = 'left')
            if self.lenCheckBox.getValue() == 1:
                pm.select(side1Edges)
                for x in range(    len(rootEdges)*2    ):
                    pm.polyEditEdgeFlow(adjustEdgeFlow=1, constructionHistory=0)
                    pm.pickWalk(type = 'edgeloop', direction = 'left')
                
        pm.select(oldSel)    

    def snap(self):
        haircap = self.capName.getText()
        selected = pm.ls(sl =1, fl =1)
        if pm.objExists(haircap):
            for sel in selected:
                pm.transferAttributes(str(haircap), sel ,flipUVs=0, transferPositions=1, transferUVs=0, 
                    searchMethod=0, transferNormals=1, transferColors=0, sampleSpace=0)
        else: print 'define hair cap and add to script'
        pm.delete(selected, constructionHistory = 1)
    

    def snapPivot(self):
        haircap = self.capName.getText()
        oldSel = pm.selected()
        self.transform()
        if pm.objExists(haircap):
            geo = pm.ls(haircap)[0]
            for sel in pm.selected():
                point = geo.getClosestPoint(sel.getTranslation())
                pm.move( point[0][0], point[0][1], point[0][2], sel)
            pm.select(oldSel)
        else: pm.error('hair cap doesnt exist in scene')
    
    
    def transform(self):
        for sel in pm.selected():
            if not pm.selected()[0].nodeType() == "transform" :
                pm.select(pm.listRelatives(pm.ls(o=1, sl=1),type='transform',p=True))
    
    
    def transfer(self):
        haircap = self.capName.getText()
        oldSel = pm.ls(sl = 1)
        pm.select(pm.ls(o=1, sl=1))
        selected = pm.ls(sl = 1)
        pm.select(cl = 1)
        myCurrentUvSet =  pm.polyUVSet(selected[0], q = True , currentUVSet = True )[0]
        if pm.objExists(haircap) and self.transferCheckBox.getValue() == 1:
            for object in selected:
                pm.transferAttributes(haircap, object, sampleSpace=0,transferUVs=1, transferColors=0, sourceUvSet = 'map1',targetUvSet = 'map1')
        elif len(selected) > 1 and self.transferCheckBox.getValue() == 0:
            last = selected.pop(-1)
            for object in selected:
                if pm.polyEvaluate(object, v = 1) ==  pm.polyEvaluate(last, v = 1):
                    pm.select([last, object])
                    pm.transferAttributes(sampleSpace=5,transferUVs=1, transferColors=0,sourceUvSet = myCurrentUvSet, targetUvSet = myCurrentUvSet )
        else: pm.error( "assign hair cap geo, or select more than one object with same topology")
        pm.select(oldSel)
        
        
    def UVFix(self):
        oldSel = pm.ls(sl = 1)
        selected = pm.ls(sl = 1, o = 1)
        pm.select(cl = 1)
        for s in selected:
            #############get info from other nodes
            myCurrentUvSet =  pm.polyUVSet(s, q = True , currentUVSet = True )[0]
            pair1, pair2 = self.findTips(s, myCurrentUvSet)
            ###############select and store roots and tips
            tipsUV = []
            rootEdges =  pm.ls(    pm.polySelect(    s, ass = 1 ,shortestEdgePath = (pair2[0].index(), pair2[1].index()    )    ), fl = 1)
            tipsUV.append(  pm.ls(  pm.polyListComponentConversion(  rootEdges, fe =1, tuv =1), fl = True  )    )
            tipEdges =  pm.ls(    pm.polySelect(    s,  ass = 1 ,shortestEdgePath = (pair1[0].index(), pair1[1].index()    )    ), fl = 1)
            tipsUV.append(  pm.ls(  pm.polyListComponentConversion(  tipEdges, fe =1, tuv =1),  fl = True )    )
            #########select and unfold the middle part of the mesh
            pm.select(  pm.ls(tipsUV, fl = 1), replace = True  )
            pm.runtime.InvertSelection()
            if self.squareCheckBox.getValue() == 1:
                pm.unfold(ps=0, us=False, i=4312, gmb=0.9457, pub=0, oa=1, ss=15.5797, gb=0.7597)
                ###########selecting length boarders
                side1 = pm.ls(pm.polySelect(ebp = [  tipEdges[0].index(), rootEdges[0].index()], ass = True ), fl = 1)
                side1 = [n for n in side1 if n not in rootEdges and n not in tipEdges]
                side2 = pm.ls(pm.polySelect(ebp = [  tipEdges[-1].index(), rootEdges[-1].index()], ass = True ), fl = 1)
                side2 = [n for n in side2 if n not in rootEdges and n not in tipEdges]
                ##########calculate all the averages
                boarder1Avg = self.tupleAvg([pair1[0].getUV(uvSet = myCurrentUvSet), pair2[0].getUV(uvSet = myCurrentUvSet)])
                boarder2Avg = self.tupleAvg([pair1[1].getUV(uvSet = myCurrentUvSet), pair2[1].getUV(uvSet = myCurrentUvSet)])
                islandAvg = self.tupleAvg([boarder1Avg, boarder2Avg])
                #########straighten length boarders
                for x in side1:
                    pm.polyEditUV(x,  u = boarder1Avg[0], r = False, uvSetName = myCurrentUvSet)
                for x in side2:
                    pm.polyEditUV(x,  u = boarder2Avg[0],  r = False, uvSetName = myCurrentUvSet)
                ##########get the perimeter of the uv island
                borderUVs = ['{}.map[{}]'.format(s,x.getUVIndices()[0]) for x in pm.ls(s.vtx, fl = 1) if x.isOnBoundary()]
                pm.select(borderUVs)
                pm.runtime.InvertSelection()
                pm.Unfold3D(pm.selected(),rs=2, ite=0, bi=1, p=0, u=1, ms=1024, tf=1)
            else: pm.Unfold3D(pm.selected(),rs=2, ite=0, bi=1, p=0, u=1, ms=1024, tf=1)
        pm.select(oldSel)
        
##########################processing helper functions: traverse verts, getFaceNormals, computeFrame, restoeTransforms
    
    def traverse( self, start , listToWalk , multiplyBy ):
        ########moves to the next vertes in the list untill stopped
        traversed = []
        for x in range(int(len(listToWalk)*multiplyBy)):
            traversed.append(start)
            neighbours = start.connectedVertices()
            for n in neighbours:
                if n in listToWalk:
                    if n not in traversed:
                        start = n
                else:
                    traversed.append(n)
        return start, traversed
    
    
    def getFaceNormals(self, faceList):
        norm = pm.dt.Vector()
        for face in faceList:
            norm += face.getNormal(space = 'object')
        return norm/len(faceList)

    
    def matrix_from_normal(self, up_vect, front_vect):
        # normalize first!
        upNorm = up_vect.normal()
        frontNorm = front_vect.normal()
        
        #get the third axis with the cross vector    
        side_vect = pm.dt.Vector.cross(frontNorm, upNorm)
        #recross in case up and front were not originally orthoganl:
        front_vect = pm.dt.Vector.cross(side_vect, upNorm )
        #the new matrix is 
        return pm.dt.TransformationMatrix (
            side_vect.x, side_vect.y, side_vect.z, 0,
            up_vect.x, up_vect.y, up_vect.z, 0,
            front_vect.x, front_vect.y, front_vect.z, 0,
            0,0,0,1)

    
    def vecAvg(self, vecList):
        #### takes in list of vectors returns an average in vector form
        sum = pm.dt.Vector()
        for point in vecList:
            sum += point
        return sum/len(vecList)
    
    def tupleAvg(self, tupleList):
        #### takes in list of vectors returns an average in vector form
        sum = [0, 0]
        for lst in tupleList:
            sum[0] += lst[0]
            sum[1] += lst[1]
        return [sum[x]/len(tupleList) for x in range(2)]
    
    def randomize(self, list, transRot):
        list = pm.ls(list, fl = True)
        rt = self.randSliderT.getValue()
        rr = self.randSliderR.getValue()
        for x in list:
            if transRot == 2 or transRot == 0:
                pm.move(str(x), random.uniform(-rt*self.TXCheckBox.getValue(),rt*self.TXCheckBox.getValue()), \
                random.uniform(-rt*self.TYCheckBox.getValue(),rt*self.TYCheckBox.getValue()), \
                random.uniform(-rt*self.TZCheckBox.getValue(),rt*self.TZCheckBox.getValue()),  relative = True)
            if transRot == 2 or transRot == 1:
                pm.rotate(str(x), [random.uniform(-rr*self.RXCheckBox.getValue(),rr*self.RXCheckBox.getValue()),\
                 +random.uniform(-rr*self.RYCheckBox.getValue(),rr*self.RYCheckBox.getValue()),\
                  +random.uniform(-rr*self.RZCheckBox.getValue(),rr*self.RZCheckBox.getValue())], relative = True )
    
    def randomTransformSel(self, myList):
        amount = int((1.0-self.randSliderT.getValue()/10) * len(myList))
        result = []
        for x in range(amount):
            myList.pop(random.randint(0, len(myList)-1))
        pm.select(cl = 1)
        pm.select(myList)

######################calculation heavy functions: set pivot, fill in between hair cards
    
    def pivot(self):   
        oldSel = pm.selected()
        self.transform()
        selected = pm.selected()
        pm.delete(selected, constructionHistory = 1)
        pm.select(clear = 1)
        for s in selected:
            #remove previous transformation data
            pm.makeIdentity(s, apply = 1)
            ###get root faces from root edges
            root = self.root(s)
            rootFaces = pm.ls(pm.polyListComponentConversion(root, fe =1, tf =1), fl = True)
            pm.select(cl = 1)
            #get list of vertices contained in the faces
            points = []
            for face in rootFaces:
                point = face.getPoints()
                for p in point:
                    if p not in points:
                        points.append(p)
            #get average from point list and put it on the surface of the geo
            faceAvg = s.getClosestPoint(self.vecAvg(points))
            #move pivots to face average
            pm.xform(s, piv = faceAvg[0], ws = 1)
            #move geo to origin to restore transformations
            pm.move( 0,0,0, s, rpr=1 )
            pos = pm.xform( s, q=1, t=1 )
            pm.makeIdentity(s, apply = 1 )
            #build matrix out of normal and  side vectors
            faceNormal = self.getFaceNormals(rootFaces)
            rootVerts = pm.ls(pm.polyListComponentConversion(root, fe =1, tv =1), fl = True)
            rotVertCoords = [x.getPosition(space = 'object') for x in rootVerts]
            avgBasePos = self.vecAvg(rotVertCoords)
            mat = self.matrix_from_normal ( faceNormal, avgBasePos)
            #rotate to align to scene axis
            pm.xform(s, matrix = mat.asMatrixInverse())
            pm.makeIdentity(s, apply = 1)
            pm.xform(s, matrix = mat)
            pm.setAttr( '%s.t' % s, pos[0]*-1,pos[1]*-1,pos[2]*-1)
            if pm.polyEvaluate(s, f = True)<2:
                pm.xform( s, piv = (   avgBasePos   ), ws = 0 )
        pm.select(oldSel)     
        
    
    def fill(self, times ):
        self.transform()
        selected = pm.ls(sl = 1)
        pm.select(cl = 1)
        if len(selected) >= 1:
            haircap = self.capName.getText()
            if len(selected) > 1:
                allNewHairs = []
                for n in range(len(selected)-1):
                    hair1 = selected[n]
                    hair2 = selected[n+1]
                    grp = pm.group(empty = True, name = 'HairGrp')
                    selfMatrix = selected[n].getMatrix()
                    hair2Matrix = selected[n+1].getMatrix()
                    grpMatrix = (selfMatrix + hair2Matrix)/2
                    grpMatrix = grpMatrix.homogenize()
                    grp.setMatrix(grpMatrix)
                    pm.parent([hair1, hair2], grp)
                    newHairs = []
                    for x in range(times-1):
                        newHair = pm.duplicate(hair1)[0]
                        newHair.setMatrix((selfMatrix*grpMatrix.inverse()).blend((hair2Matrix*grpMatrix.inverse()), weight = (x+1)*(1.0/times)))
                        #set blendshapes connecting new hair with the original hair
                        pm.blendShape(     hair1 ,newHair , w = (    0 , 1-(    (x+1)*(1.0/times)    )    )    )
                        #if hairs are the same connect the last one as well
                        if pm.polyEvaluate(hair1, v=1) == pm.polyEvaluate(hair2, v=1):
                            pm.blendShape(     hair2 ,newHair , w = (    0 , (x+1)*(1.0/times)    )    )
                        if pm.objExists(haircap) and self.transferCheckBox.getValue() == 1 :
                            pm.transferAttributes(haircap, newHair, sampleSpace=0,transferUVs=1, transferColors=0, sourceUvSet = 'map1',targetUvSet = 'map1')
                        newHairs.append(newHair)
                    pm.ungroup(grp)
                    allNewHairs.append(newHairs)
                if self.randSliderT.getValue() or self.randSliderR.getValue() > 0:
                    self.randomize(allNewHairs, transRot = 2)
                pm.select(allNewHairs)
            else:
                hair1 = selected[0]
                newHairs = []
                for x in range(times-1):
                    newHair = pm.duplicate(hair1)[0]
                    selfTrans = newHair.getTranslation()
                    selfRot = newHair.getRotation()
                    newHairs.append(newHair)
                if self.randSliderT.getValue() or self.randSliderR.getValue() > 0:
                    self.randomize(newHairs, transRot = 2)
                pm.select(newHairs)
        else: pm.error( "select something")

    
    
HairGrabberUI()