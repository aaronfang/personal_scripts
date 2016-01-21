# issues:
#	- remove from blendshapeList
#	- 
import pymel.core as pm

class blendshapeUI(object):
	def __init__(self):
		self.meshWithBS = ""
		self.bsNd = []
		pass
	
	def _UI(self):
		if pm.window("blendshapeWin",exists=1):
			pm.deleteUI("blendshapeWin",window=1)
		w=450
		w2=190
		
		self.window=pm.window("blendshapeWin",t="BlendShape Tools",s=0,mb=1,rtf=1,w=w)
		h=pm.window("blendshapeWin",q=1,h=1)
		
		pm.columnLayout("mainColumn",p="blendshapeWin",columnAttach=('both', 2), rowSpacing=10, columnWidth=w)
		'''
		pm.button(p="mainColumn",l="abSymMesh",c=self.abSymMeshFunc)
		
		pm.frameLayout("mirrorSepShapeFrame",p="mainColumn", label='Mirror Separated Shapes', borderStyle='in',cll=1)
		pm.rowLayout("oldNewTextRow",p="mirrorSepShapeFrame",w=w,numberOfColumns=2,columnWidth2=(w2,w2),adjustableColumn=2, columnAlign2=[('center'),('center')], columnAttach=[(1, 'both', 0), (2, 'both', 0)])
		pm.button(p="oldNewTextRow",l="New Shape")
		pm.button(p="oldNewTextRow",l="Old Shape")
		pm.rowLayout("oldNewShapeRow",p="mirrorSepShapeFrame",w=w,numberOfColumns=2,columnWidth2=(w2,w2),adjustableColumn=2, columnAlign2=[('center'),('center')], columnAttach=[(1, 'both', 0), (2, 'both', 0)])
		pm.textScrollList("newSpList",p="oldNewShapeRow",w=w2,numberOfRows=1, allowMultiSelection=False)
		pm.textScrollList("oldSpList",p="oldNewShapeRow",w=w2,numberOfRows=1, allowMultiSelection=False)
		
		pm.button(p="mirrorSepShapeFrame",l="Mirror Shape")
		'''
		
		# ----------------------------------------------------------------------------------------

		pm.frameLayout("updateShapeFrame",p="mainColumn", label='Update Shapes', borderStyle='in',cll=1,cc=self.resizeWin4UpdateShape,ec=self.resizeWin4UpdateShape)
		pm.rowLayout("ShapeNamesRow",p="updateShapeFrame",w=w,numberOfColumns=3,columnWidth3=(w2,30,w2),adjustableColumn=2, columnAlign3=[('center'),('center'),('center')], columnAttach=[(1, 'both', 1), (2, 'both', 0), (3, 'both',5)])
		pm.button(p="ShapeNamesRow",l="New Shapes",c=self.newShapeList)
		pm.text(p="ShapeNamesRow",l=" ")
		pm.button(p="ShapeNamesRow",l="Current Shapes",c=self.curShapeList)
		
		pm.rowLayout("shapeListRow",p="updateShapeFrame",w=w,numberOfColumns=3,columnWidth3=(30,30,30),adjustableColumn=2, columnAlign3=[('center'),('center'),('center')], columnAttach=[(1, 'both', 1), (2, 'both', 0), (3, 'both',5)])
		pm.textScrollList("newShapeList",p="shapeListRow",w=w2,numberOfRows=8, allowMultiSelection=True)
		pm.popupMenu("newShapelistPopUp",p="newShapeList")
		pm.menuItem(p="newShapelistPopUp",l="Add To List",c=self.newShapeList)
		pm.menuItem(p="newShapelistPopUp",l="Remove All From List",c=self.rmvAllFromNewList)

			
		self.button=pm.button(p="shapeListRow",l="update",c=self.updateShape)
		
		pm.textScrollList("curShapeList",p="shapeListRow",w=w2,numberOfRows=8, allowMultiSelection=True)
		pm.popupMenu("curShapelistPopUp",p="curShapeList")
		pm.menuItem(p="curShapelistPopUp",l="Add To List",c=self.curShapeList)
		pm.menuItem(p="curShapelistPopUp",l="Remove All From List",c=self.rmvAllFromCurList)

		#---------------------------------------------------------------------

		pm.frameLayout("stripShapesFrame",p="mainColumn", label='Strip Shapes', borderStyle='in',cll=1,cc=self.resizeWin4StripShape,ec=self.resizeWin4StripShape)
		pm.button(p="stripShapesFrame",l="Get BlendShapes",c=self.getBlendShapes)
		pm.rowLayout("stripShapesRow",p="stripShapesFrame",w=w,numberOfColumns=2,columnWidth2=(30,30),adjustableColumn=2, columnAlign2=[('center'),('center')], columnAttach=[(1, 'both', 0), (2, 'both', 0)])
		pm.textScrollList("blendshapeList",p="stripShapesRow",w=140,numberOfRows=8, allowMultiSelection=False,sc=self.getTargetShapes)
		pm.popupMenu("blendShapeListPopUp",p="blendshapeList")
		pm.menuItem(p="blendShapeListPopUp",l="Remove All From List",c=self.rmvAllFromblendShapeList)
		
		pm.textScrollList("targetShapeList",p="stripShapesRow",w=140,numberOfRows=8, allowMultiSelection=True)	

		self.button=pm.button(p="stripShapesFrame",l="Strip Shapes",c=self.stripShapes)

		
		pm.showWindow(self.window)

	def resizeWin4UpdateShape(self,*args):
		updateShapeFrameState = pm.frameLayout("updateShapeFrame",q=1,cl=1)
		stripShapeFrameState = pm.frameLayout("stripShapesFrame",q=1,cl=1)

		if updateShapeFrameState == 1 and stripShapeFrameState == 1:
			pm.window("blendshapeWin",e=1,h=(h-159-192))
		elif updateShapeFrameState == 0 and stripShapeFrameState == 0:
			pm.window("blendshapeWin",e=1,h=h)
		elif updateShapeFrameState == 1 and stripShapeFrameState == 0:
			pm.window("blendshapeWin",e=1,h=(h-159))
		elif updateShapeFrameState == 0 and stripShapeFrameState == 1:
			pm.window("blendshapeWin",e=1,h=(h-192))

	def resizeWin4StripShape(self,*args):
		updateShapeFrameState = pm.frameLayout("updateShapeFrame",q=1,cl=1)
		stripShapeFrameState = pm.frameLayout("stripShapesFrame",q=1,cl=1)

		if updateShapeFrameState == 1 and stripShapeFrameState == 1:
			pm.window("blendshapeWin",e=1,h=(h-159-192))
		elif updateShapeFrameState == 0 and stripShapeFrameState == 0:
			pm.window("blendshapeWin",e=1,h=h)
		elif updateShapeFrameState == 1 and stripShapeFrameState == 0:
			pm.window("blendshapeWin",e=1,h=(h-159))
		elif updateShapeFrameState == 0 and stripShapeFrameState == 1:
			pm.window("blendshapeWin",e=1,h=(h-192))

	def abSymMeshFunc(self,*args):
		pm.mel.eval("source abSymMesh;abSymMesh;")

	def mirrorSepratedShapes(self,*args):
	   
		geo = cmds.ls(sl=1,fl=1)
		
		if 'L_' in geo[0]:
		    print 'Mirroring from Left to Right'
		    side='left'
		    Lgeo=geo[0]
		    Rgeo=Lgeo.replace('L_', 'R_')
		   
		if 'R_' in geo[0]:
		    print 'Mirroring from Right to Left'
		    side='right'
		    Rgeo=geo[0]
		    Lgeo=Rgeo.replace('R_', 'L_')     
		 
		Lshape=cmds.listRelatives(Lgeo, shapes=True, type='mesh', ni=True)
		Rshape=cmds.listRelatives(Rgeo, shapes=True, type='mesh', ni=True)
		
		Lvert=cmds.polyEvaluate(Lshape[0], v=True)
		Rvert=cmds.polyEvaluate(Rshape[0], v=True) 
		
		if not Lvert==Rvert:
		    print 'Vertex count not matching between the two sides'
		   
		if side=='left':
		    base=Lgeo
		    target=Rgeo
		   
		if side=='right':
		    base=Rgeo
		    target=Lgeo
		
		for i in range(0,Lvert):
		    #print('%s.vtx[%d]'%(Lgeo,i))
		    pos=cmds.xform(('%s.vtx[%d]'%(base,i)), q=True, ws=True, t=True)
		    cmds.xform(('%s.vtx[%d]'%(target,i)), t=((pos[0]*-1),pos[1],pos[2]), ws=True)

	def curShapeList(self,*args):
		getSel = pm.ls(sl=1,fl=1)
		listItems = pm.textScrollList("curShapeList",q=1,ai=1)
		if len(getSel)>=1:
			if len(listItems) == 0:
				pm.textScrollList("curShapeList",e=1,append=getSel)
			elif len(listItems) >= 1:
				for sel in getSel:
					if sel not in listItems:
						pm.textScrollList("curShapeList",e=1,append=sel)
	
	
	def newShapeList(self,*args):
		getSel = pm.ls(sl=1,fl=1)
		listItems = pm.textScrollList("newShapeList",q=1,ai=1)
		if len(getSel)>=1:
			if len(listItems) == 0:
				pm.textScrollList("newShapeList",e=1,append=getSel)
			elif len(listItems) >= 1:
				for sel in getSel:
					if sel not in listItems:
						pm.textScrollList("newShapeList",e=1,append=sel)
	
	def rmvAllFromCurList(self,*args):
		pm.textScrollList("curShapeList",e=1,ra=1)
	
	def rmvAllFromNewList(self,*args):
		pm.textScrollList("newShapeList",e=1,ra=1)
			
	def updateShape(self,*args):
		newShapes = pm.textScrollList("newShapeList",q=1,ai=1)
		curShapes = pm.textScrollList("curShapeList",q=1,ai=1)
		if len(newShapes) == len(curShapes) and len(curShapes)>0:
			for i,x in enumerate(curShapes):
				bsNd = pm.blendShape(newShapes[i],x)
				pm.setAttr(bsNd[0]+'.'+newShapes[i],1)
				pm.select(x,r=1)
				pm.delete(x,ch=1)
				pm.textScrollList("newShapeList",e=1,ri=newShapes[i])
				pm.setAttr('{0}.visibility'.format(newShapes[i]),0) #pm.delete(newShapes[i])

	def getBlendShapes(self,*args):
		getSel = pm.ls(sl=1,fl=1)
		if len(getSel) == 1:
			self.meshWithBS = getSel[0]
			bsNd = pm.ls(pm.listHistory(getSel[0]) or [],type='blendShape')
			itemInList = pm.textScrollList("blendshapeList",q=1,ai=1)
			if len(itemInList)>0:
				for x in bsNd:
					if x not in itemInList:
						listItems = pm.textScrollList("blendshapeList",e=1,append=x)
			else:
				listItems = pm.textScrollList("blendshapeList",e=1,append=bsNd)

	def rmvAllFromblendShapeList(self,*args):
		pm.textScrollList("blendshapeList",e=1,ra=1)
		pm.textScrollList("targetShapeList",e=1,ra=1)

	def getTargetShapes(self,*args):
		pm.textScrollList("targetShapeList",e=1,ra=1)
		self.bsNd = pm.textScrollList("blendshapeList",q=1,si=1)
		if len(self.bsNd) == 1:
			tgtShapes = pm.blendShape(self.bsNd[0],t=1,q=1)
			if len(tgtShapes)>0:
				listTarget = pm.textScrollList("targetShapeList",e=1,append=tgtShapes)

	def stripShapes(self,*args):
		mesh = self.meshWithBS
		if len(self.bsNd) == 1:
			tgtShapes = pm.textScrollList("targetShapeList",q=1,si=1)
			if len(tgtShapes)>0:
				newShapeGrp = pm.group(n=(mesh+'_faceshapes'),em=1)
				for tgt in tgtShapes:
					pm.setAttr(self.bsNd[0]+'.'+tgt,1)
					newTgt = pm.duplicate(mesh,n=tgt)
					pm.parent(newTgt,newShapeGrp)
					pm.setAttr(self.bsNd[0]+'.'+tgt,0)
				pm.select(newShapeGrp,r=1)


	
blendshapeUI()._UI()
