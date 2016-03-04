if cmds.hotkeySet('Aaron_hotkey',ex=True) and cmds.hotkeySet(q=True,cu=True)!='Aaron_hotkey':
    cmds.hotkeySet('Aaron_hotkey',edit=True,current=True)
    print "The current hotkey set is: \"{0}\"".format(cmds.hotkeySet(q=True,cu=True))
else:print "The current hotkey set is: \"{0}\"".format(cmds.hotkeySet(q=True,cu=True))
