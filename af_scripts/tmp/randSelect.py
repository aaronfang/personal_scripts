# Shuffle a list then separate it into certain parts.
# Usage: randomSplitList().randListFunc(list,parts)
# will return a list contains separated parts for use.
import pymel.core as pm
import random

class randomSplitList(object):
	def __init__(self):
		self.list,self.cols,self.randList,self.newList = list,cols,randList,newList
		self.list=[]
		self.cols=1
		self.randList=[]
		self.newList=[]

	def splitList(self,list,cols):
		start = 0
		newList = []
		for i in xrange(cols):
			stop = start + len(list[i::cols])
			newList.append(list[start:stop])
			start = stop
		return newList

	def randListFunc(self,list,cols):
		randList = list
		random.shuffle(randList)
		newList = self.splitList(randList,cols)
		return newList

class randListUI(object):
	def __init__(self):
		pass
	
	def _UI(self):
		if pm.window("mainWin",exists=1):
			pm.deleteUI("mainWin",window=1)
		
		w=280
		
		window=pm.window("mainWin",t="Shuffle Select Tool",s=0,mb=1,mnb=0,mxb=0,rtf=1,w=w)
		pm.columnLayout("mainColumn",p="mainWin",columnAttach=('both', 2), rowSpacing=10, columnWidth=w)
		pm.text(l="Slice selection into random parts")
		pm.intSliderGrp("colsSlider",p="mainColumn",cw3=(30,45,50),field=True,label='Parts',minValue=1,maxValue=5,fieldMinValue=1,value=1,step=1)
		pm.radioButtonGrp("radioBtnGrp",l=" ",labelArray2=['List', 'Group'],cw3=[60,90,80],numberOfRadioButtons=2,sl=1)
		
		pm.textScrollList("listScroll",p="mainColumn",numberOfRows=5, allowMultiSelection=False,sc=)
		
		pm.button(p="mainColumn",l="Shuffle")

		pm.showWindow("mainWin")
	
	def shuffleSlice(self,*args):
		getSel = pm.ls(sl=1,fl=1)
		cols = pm.intSliderGrp("colsSlider",q=1,v=1)
		if len(getSel)>=1 and len(getSel)>=cols:
			array = getSel
			self.result = randomSplitList().randListFunc(array,cols)
			if pm.radioButtonGrp("radioBtnGrp",q=1,sl=1) == "List":
				pm.textScrollList("listScroll",e=1,ra=1)
				for i in range(0,len(self.result)):
					pm.textScrollList("listScroll",e=1,append="{0},{1}".format("Part-",(i+1)))
	
	def selPart(self,*args):
		if pm.textScrollList("listScroll",q=1,si=1)
randListUI()._UI()



pm.select(randomSplitList().randListFunc(a,4)[0],r=1)
a=pm.ls(sl=1,fl=1)
