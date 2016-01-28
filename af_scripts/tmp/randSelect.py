# Shuffle a list then separate it into certain parts.
# Usage: randomSplitList().randListFunc(list,parts)
# will return a list contains separated parts for use.
import pymel.core as pm
import random

class randomSplitList(object):
	def __init__(self):
		list=[]
		cols=1
		randList=[]
		newList=[]
		self.list,self.cols,self.randList,self.newList = list,cols,randList,newList

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
		
		window=pm.window("mainWin",t="Shuffle Slice Tool",s=0,mb=1,mnb=0,mxb=0,rtf=1,w=w)
		pm.columnLayout("mainColumn",p="mainWin",columnAttach=('both', 2), rowSpacing=10, columnWidth=w)
		pm.text("warningText",p="mainColumn",l="---===Select something to slice===---",al="center")
		pm.intSliderGrp("colsSlider",p="mainColumn",cw3=(30,45,50),field=True,label='Parts',minValue=1,fieldMinValue=1,value=1,fs=1,ss=1)
		pm.radioButtonGrp("radioBtnGrp",l=" ",labelArray2=['List', 'Group'],cw3=[60,90,80],numberOfRadioButtons=2,sl=1)
		
		pm.textScrollList("listScroll",p="mainColumn",numberOfRows=5, allowMultiSelection=False,sc=self.selPart)
		pm.popupMenu("listPopUp",p="listScroll")
		pm.menuItem(p="listPopUp",l="Create Group for the parts",c=self.groupPartsFunc)
		
		pm.button(p="mainColumn",l="Shuffle Slice",c=self.shuffleSlice)
		

		pm.showWindow("mainWin")
	
	def shuffleSlice(self,*args):
		getSel = pm.ls(sl=1,fl=1)
		cols = pm.intSliderGrp("colsSlider",q=1,v=1)
		if len(getSel)>=1 and len(getSel)>=cols:
			array = getSel
			self.result = randomSplitList().randListFunc(array,cols)
			if pm.radioButtonGrp("radioBtnGrp",q=1,sl=1) == 1:
				pm.text("warningText",e=1,l="---===List All Parts===---")
				pm.textScrollList("listScroll",e=1,ra=1)
				for i in range(0,len(self.result)):
					pm.textScrollList("listScroll",e=1,append="{0}{1}".format("ShuffledPart_",(i+1)))
			elif pm.radioButtonGrp("radioBtnGrp",q=1,sl=1) == 2:
				pm.textScrollList("listScroll",e=1,ra=1)
				allGrps=[]
				for i in range(0,len(self.result)):
					grp = pm.group(n=("{0}{1}".format("ShuffledPart_",(i+1))),em=1)
					pm.parent(self.result[i],grp)
					allGrps.append(grp)
				pm.select(allGrps,r=1)
		elif len(getSel)==0:
			pm.textScrollList("listScroll",e=1,ra=1)
			pm.text("warningText",e=1,l="---===Select Something!!!===---")
		elif len(getSel)>0 and len(getSel)<cols:
			pm.textScrollList("listScroll",e=1,ra=1)
			pm.text("warningText",e=1,l="---===Too Much Parts!!!===---")
	
	def selPart(self,*args):
		curSelInList = pm.textScrollList("listScroll",q=1,si=1)
		i = curSelInList[0][-1]
		if i.isdigit():
			pm.select(self.result[(int(i)-1)],r=1)
		
	def groupPartsFunc(self,*args):
		allGrps=[]
		if len(pm.textScrollList("listScroll",q=1,ai=1))!=0:
			if len(self.result)==len(pm.textScrollList("listScroll",q=1,ai=1)):
				for i in range(0,len(self.result)):
					grp = pm.group(n=("{0}{1}".format("ShuffledPart_",(i+1))),em=1)
					pm.parent(self.result[i],grp)
					allGrps.append(grp)
				pm.select(allGrps,r=1)

		
randListUI()._UI()
