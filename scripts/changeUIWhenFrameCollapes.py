from functools import partial

def frameCollapseChanged(mainLayout):
mc.evalDeferred("mc.window('ToolUI', e=1, h=sum([eval('mc.' + mc.objectTypeUI(child) + '(\\'' + child + '\\', q=1, h=1)') for child in mc.columnLayout('" + mainLayout + "', q=1, ca=1)]))")

#check to see if window exists
if mc.window("ToolUI", exists = True):
mc.deleteUI("ToolUI")
#create window
ToolWindow = mc.window("ToolUI", title = "Tool UI", w = 300, h = 300, mnb = True, mxb = False, sizeable = False)
#create a main layout
mainLayout = mc.columnLayout (w =300)


### FIRST TAB ###
frameLayout1 = mc.frameLayout (width = 300, label = "Tab 1", collapse = True, collapsable = True, marginWidth = 5, parent = mainLayout, ec=partial(frameCollapseChanged, str(mainLayout)), cc=partial(frameCollapseChanged, str(mainLayout)))
#create a button
mc.button (label = "Button 1", w = 280, h = 50, command = 'print "hello",', parent = frameLayout1)
#create a button
mc.button (label = "Button 2", w = 280, h = 50, command = 'print "hello",', parent = frameLayout1)
#create a button
mc.button (label = "Button 3", w = 280, h = 50, command = 'print "hello",', parent = frameLayout1)


### SECOND TAB ###
frameLayout2 = mc.frameLayout (width = 300, label = "Tab 2", collapse = True, collapsable = True, marginWidth = 5, parent = mainLayout, ec=partial(frameCollapseChanged, str(mainLayout)), cc=partial(frameCollapseChanged, str(mainLayout)))
#create a button
mc.button (label = "Button 4", w = 280, h = 50, command = 'print "hello",', parent = frameLayout2)
#create a button
mc.button (label = "Button 5", w = 280, h = 50, command = 'print "hello",', parent = frameLayout2)
#create a button
mc.button (label = "Button 6", w = 280, h = 50, command = 'print "hello",', parent = frameLayout2 )

#show window
mc.showWindow(ToolWindow)


I added a function that gets called every time one of the frames is collapsed or expanded. It gets all the children of the main layout, adds up their height, and then changes the window height. Here is what it's doing, without the eval deferred or list comprehension:

winHeight = 0
# iterate through all children of the main layout
for child in mc.columnLayout(mainLayout, q=1, ca=1):
# for each child, get it's type, then use that run an eval command to get that ui item's height and add it to the height variable
winHeight += eval('mc.' + mc.objectTypeUI(child) + '("' + child + '", q=1, h=1)')
# set the window height with the gathered height values
mc.window('ToolUI', e=1, h=winHeight)