from PySide import QtGui, QtCore
 
def removeInvalidClipboardData():
    oldMimeData = QtGui.qApp.clipboard().mimeData()
    newMimeData = QtCore.QMimeData()
    for format in oldMimeData.formats():
        if 'text/uri-list' in format: #This breaks maya paste
            continue
        data = oldMimeData.data(format)
        newMimeData.setData(format, data)
    clipboard = QtGui.qApp.clipboard() 
    clipboard.blockSignals(True)
    clipboard.setMimeData(newMimeData)
    clipboard.blockSignals(False)
QtGui.qApp.clipboard().dataChanged.connect(removeInvalidClipboardData)
