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
		if pm.window('mainWin',exist=1):
			pm.deleteUI('mainWin',window=1)
		
		window=pm.window('mainWin',t="

pm.select(randomSplitList().randListFunc(a,4)[0],r=1)
a=pm.ls(sl=1,fl=1)
