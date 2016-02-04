# This tool is design for the modeler to layout their UVs in more efficient way.
# - Line up UVs based on object level to 'U' or 'V' direction with a certain gap provided.
# - Layout UVs based on object level to each UDIMs
# - RoadKill Pro plugin functions
# - store and select a list of objects


import pymel.core as pm
import math

class lineUpUVs(object):
	def __init__(self):
		self.Sels=[]
		self.W=[]
		self.H=[]
		self.Sels=[]
		pass
	
	def _UI(self):
		if pm.window("lineUpWin",exists=1):
			pm.deleteUI("lineUpWin",window=1)
		w=180
		self.window=pm.window("lineUpWin",t="AlignUVs",s=0,mb=1,rtf=1,wh=(w,25))

		pm.columnLayout("mainColumn",p="lineUpWin",columnAttach=('both', 2), rowSpacing=10, columnWidth=w)
		pm.rowLayout(p="mainColumn",w=w,h=25,numberOfColumns=4,columnWidth4=(30,30,30,40),adjustableColumn=1, columnAlign=(1, 'right'), columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0), (4, 'both', 0)])
		self.floatField=pm.floatField("gapValueField",v=0.003)
		self.button=pm.button(l="U",c=self.lineUpU)
		self.button=pm.button(l="V",c=self.lineUpV)
		self.button=pm.button(l="UDIM",c=self.layoutUVsToUDIM)
		
		pm.separator(p="mainColumn",style='in')
		pm.rowLayout(p="mainColumn",w=w,h=25,numberOfColumns=4,columnWidth4=(30,30,30,40),adjustableColumn=1, columnAlign=(1, 'right'), columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0), (4, 'both', 0)])
		self.button=pm.button(l="Scale2Src",c=self.RK_ScaleToSrc)
		self.button=pm.button(l="G",c=self.RK_Geometric)
		self.button=pm.button(l="O",c=self.RK_Organic)
		self.button=pm.button(l="S",c=self.RK_Straighten)

		pm.separator(p="mainColumn",style='in')
		pm.rowLayout(p="mainColumn",w=w,h=25,numberOfColumns=3,columnWidth3=(10,30,80),adjustableColumn=1, columnAlign=(1, 'right'), columnAttach=[(1, 'both', 5), (2, 'both', 0),(3, 'both', 5)])
		pm.text("Pixel Ratio",al="left")
		pm.intField("ratioFld",value=50)
		pm.button(l="Rescale UVs",c=self.scaleUVRatio)

		pm.separator(p="mainColumn",style='in')
		pm.button(p="mainColumn",l="Store Selection",c=self.storeSelToList)
		pm.textScrollList("selListTextScroll",p="mainColumn",numberOfRows=5, allowMultiSelection=True)
		pm.popupMenu("listPopUp",p="selListTextScroll")
		pm.menuItem(p="listPopUp",l="Select All In List",c=self.selectAllInList)
		pm.menuItem(p="listPopUp",l="Remove Selected From List",c=self.rmvSelFromList)
		pm.menuItem(p="listPopUp",l="Remove All From List",c=self.rmvAllFromList)
		
		pm.button(p="mainColumn",l="Select",c=self.selectHighlightedInList)

		pm.showWindow(self.window)
		
	def layoutUVsToUDIM(self,*args):
		sels = pm.ls(sl=1)
		for i, x in enumerate(sels):
			x=x.getShape()
			pm.select('{0}.map[:]'.format(x), r=1)
			pm.polyEditUV(u=i % 10, v=int(math.floor(i / 10)))
		pm.select(sels,r=1)

	def lineUpU(self,*args):
		sels = pm.ls(sl=1)
		gap = pm.floatField("gapValueField",q=True,v=True)
		
		for x in sels:
			x=x.getShape()
			pm.select('{0}.map[:]'.format(x), r=1)
			buv = pm.polyEvaluate(x,b2=1)
			w = abs(buv[0][1] - buv[0][0])
			self.W.append(w)
			
		for i, x in enumerate(sels):
			initGap = 0.003
			x=x.getShape()
			pm.select('{0}.map[:]'.format(x), r=1)
			buv = pm.polyEvaluate(x,b2=1)
			if i==0:
				pm.polyEditUV(u=-buv[0][0]+initGap,v=-buv[1][0]+initGap)
			else:
				width = sum(self.W[0:i])
				pm.polyEditUV(u=-buv[0][0]+initGap+width+gap*i,v=-buv[1][0]+initGap)
		pm.select(sels,r=1)
		self.W=[]

	def lineUpV(self,*args):
		sels = pm.ls(sl=1)
		gap = pm.floatField("gapValueField",q=True,v=True)
		
		for x in sels:
			x=x.getShape()
			pm.select('{0}.map[:]'.format(x), r=1)
			buv = pm.polyEvaluate(x,b2=1)
			h = abs(buv[1][1] - buv[1][0])
			self.H.append(h)
			
		for i, x in enumerate(sels):
			initGap = 0.003
			x=x.getShape()
			pm.select('{0}.map[:]'.format(x), r=1)
			buv = pm.polyEvaluate(x,b2=1)
			if i==0:
				pm.polyEditUV(v=-buv[1][1]-initGap,u=-buv[0][0]+initGap)
			else:
				width = sum(self.H[0:i])
				pm.polyEditUV(v=-buv[1][1]-initGap-width-gap*i,u=-buv[0][0]+initGap)
		pm.select(sels,r=1)
		self.H=[]

	def RK_Geometric(self,*args):
		if pm.pluginInfo("Roadkill",q=1,l=1)==False:
			pm.loadPlugin("Roadkill")
		pm.mel.eval("RoadkillProGeometric")

	def RK_Organic(self,*args):
		if pm.pluginInfo("Roadkill",q=1,l=1)==False:
			pm.loadPlugin("Roadkill")
		pm.mel.eval("RoadkillProOrganic")

	def RK_Straighten(self,*args):
		if pm.pluginInfo("Roadkill",q=1,l=1)==False:
			pm.loadPlugin("Roadkill")
		pm.mel.eval("RoadkillProStraighten")

	def RK_ScaleToSrc(self,*args):
		if pm.pluginInfo("Roadkill",q=1,l=1)==False:
			pm.loadPlugin("Roadkill")
		pm.mel.eval("RoadkillProScaleToSource")
	
	def selMesh(self,*args):
		getSel = pm.ls(sl=1,fl=1)
		listItems = pm.textScrollList("selListTextScroll",q=1,ai=1)
		curSelInList = pm.textScrollList("selListTextScroll",q=1,si=1)
		if len(getSel)==0:
			if len(curSelInList)!=0:
				pm.select(curSelInList,r=1)
			else:
				pm.select(listItems,r=1)
		elif len(getSel)>=1:
			self.Sels=getSel
			newList=[]
			if len(listItems) == 0:
				pm.textScrollList("selListTextScroll",e=1,append=self.Sels)
			elif len(listItems) >= 1:
					if sel not in listItems:
						pm.textScrollList("selListTextScroll",e=1,append=sel)
	
	def storeSelToList(self,*args):
		getSel = pm.ls(sl=1,fl=1)
		listItems = pm.textScrollList("selListTextScroll",q=1,ai=1)
		if len(getSel)>=1:
			if len(listItems) == 0:
				pm.textScrollList("selListTextScroll",e=1,append=getSel)
			elif len(listItems) >= 1:
				for sel in getSel:
					if sel not in listItems:
						pm.textScrollList("selListTextScroll",e=1,append=sel)
	
	def rmvSelFromList(self,*args):
		curSelInList = pm.textScrollList("selListTextScroll",q=1,si=1)
		pm.textScrollList("selListTextScroll",e=1,ri=curSelInList)

	def rmvAllFromList(self,*args):
		pm.textScrollList("selListTextScroll",e=1,ra=1)		

	def selectHighlightedInList(self,*args):
		curSelInList = pm.textScrollList("selListTextScroll",q=1,si=1)
		listItems = pm.textScrollList("selListTextScroll",q=1,ai=1)
		if len(curSelInList)>0:
			pm.select(curSelInList,r=1)
		elif len(curSelInList)==0:
			pm.select(listItems,r=1)

	def selectAllInList(self,*args):
		listItems = pm.textScrollList("selListTextScroll",q=1,ai=1)
		pm.textScrollList("selListTextScroll",e=1,si=listItems)

	def scaleUVRatio(self,*args):
		res = 1024
		mult = 1
		mult = (mult*(8192/res))/8
		densityField = pm.intField("ratioFld",q=1,v=1)
		unfold=0.0009765625*(densityField)
		ratioField = unfold*mult
		pm.unfold(i=0,us=True,s=ratioField)

lineUpUVs()._UI()
