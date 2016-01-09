import random as rd

list = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

randList = list
#print randList

div=3

listSize=len(list)
#print listSize

numForOnePart=listSize/div
#print numForOnePart

rd.shuffle(randList)

#print randList


print [randList[i::3] for i in range(3)]
  
print randList