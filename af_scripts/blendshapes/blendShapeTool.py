import pymel.core as pm

class blendshapeUI(object):
	def __init__(self):
		self.meshWithBS = ""
		pass
	
	def _UI(self):
		if pm.window("blendshapeWin",exists=1):
			pm.deleteUI("blendshapeWin",window=1)
		w=350
		self.window=pm.window("blendshapeWin",t="BlendShape Tools",s=0,mb=1,rtf=1,w=w)

		pm.columnLayout("mainColumn",p="blendshapeWin",columnAttach=('both', 2), rowSpacing=10, columnWidth=w)
		
		pm.frameLayout("updateShapeFrame",p="mainColumn", label='Update Shapes', borderStyle='in' )
		pm.rowLayout("ShapeNamesRow",p="updateShapeFrame",w=w,numberOfColumns=3,columnWidth3=(150,30,150),adjustableColumn=2, columnAlign3=[('center'),('center'),('center')], columnAttach=[(1, 'both', 1), (2, 'both', 0), (3, 'both',5)])
		pm.button(p="ShapeNamesRow",l="New Shapes",c=self.newShapeList)
		pm.text(p="ShapeNamesRow",l=" ")
		pm.button(p="ShapeNamesRow",l="Current Shapes",c=self.curShapeList)
		
		pm.rowLayout("shapeListRow",p="updateShapeFrame",w=w,numberOfColumns=3,columnWidth3=(30,30,30),adjustableColumn=2, columnAlign3=[('center'),('center'),('center')], columnAttach=[(1, 'both', 1), (2, 'both', 0), (3, 'both',5)])
		pm.textScrollList("newShapeList",p="shapeListRow",w=140,numberOfRows=8, allowMultiSelection=True)
		pm.popupMenu("newShapelistPopUp",p="newShapeList")
		pm.menuItem(p="newShapelistPopUp",l="Add To List",c=self.newShapeList)
		pm.menuItem(p="newShapelistPopUp",l="Remove All From List",c=self.rmvAllFromNewList)

			
		self.button=pm.button(p="shapeListRow",l="update",c=self.updateShape)
		
		pm.textScrollList("curShapeList",p="shapeListRow",w=140,numberOfRows=8, allowMultiSelection=True)
		pm.popupMenu("curShapelistPopUp",p="curShapeList")
		pm.menuItem(p="curShapelistPopUp",l="Add To List",c=self.curShapeList)
		pm.menuItem(p="curShapelistPopUp",l="Remove All From List",c=self.rmvAllFromCurList)

		#---------------------------------------------------------------------

		pm.frameLayout("stripShapesFrame",p="mainColumn", label='Strip Shapes', borderStyle='in' )
		pm.button(p="stripShapesFrame",l="Get BlendShapes",c=self.getBlendShapes)
		pm.rowLayout("stripShapesRow",p="stripShapesFrame",w=w,numberOfColumns=3,columnWidth3=(30,30,30),adjustableColumn=2, columnAlign3=[('center'),('center'),('center')], columnAttach=[(1, 'both', 1), (2, 'both', 0), (3, 'both',5)])
		pm.textScrollList("blendshapeList",p="stripShapesRow",w=140,numberOfRows=8, allowMultiSelection=True)
		pm.popupMenu("newShapelistPopUp",p="blendshapeList")
		pm.menuItem(p="newShapelistPopUp",l="Add To List",c=self.newShapeList)
		pm.menuItem(p="newShapelistPopUp",l="Remove All From List",c=self.rmvAllFromNewList)

			
		self.button=pm.button(p="stripShapesRow",l="strip",c=self.stripShapes)
		
		pm.textScrollList("curShapeList",p="stripShapesRow",w=140,numberOfRows=8, allowMultiSelection=True)
		pm.popupMenu("curShapelistPopUp",p="curShapeList")
		pm.menuItem(p="curShapelistPopUp",l="Add To List",c=self.curShapeList)
		pm.menuItem(p="curShapelistPopUp",l="Remove All From List",c=self.rmvAllFromCurList)		


		
		pm.showWindow(self.window)
	
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
			listItems = pm.textScrollList("blendshapeList",e=1,append=bsNd)

	def stripShapes(self,*args):
		if len(self.meshWithBS) == 1:
			bsNd = pm.textScrollList("blendshapeList",q=1,si=1)
			if len(bsNd) == 1:
				tgtShapes = cmds.blendShape(bsNd[0],t=1,q=1)
				if len(tgtShapes)>0:
					newShapeGrp = cmds.group(n=(self.meshWithBS+'_faceshapes'),em=1)
					for tgt in tgtShapes:
						cmds.setAttr(bsNd[0]+'.'+tgt,1)
						newTgt = cmds.duplicate(self.meshWithBS,n=tgt)
						cmds.parent(newTgt,newShapeGrp)
						cmds.setAttr(bsNd[0]+'.'+tgt,0)
					pm.select(newShapeGrp,r=1)


	
blendshapeUI()._UI()
