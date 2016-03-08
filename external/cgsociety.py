import urllib
import urllib2
import re
import os
import time

def url_open(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (X11; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0')
    html = urllib2.urlopen(req)
    return html.read()
    
def saveArt(folder, pageNum, artAddrs, filename):
    try:
        print("saving "+str(pageNum)+'_'+filename+" in "+folder+'\n'+artAddrs)
        fileName = 'P'+str(pageNum)+'_'+filename+'.jpg'
        with open(fileName,'wb') as f:
            img = url_open(artAddrs)
            f.write(img)
        return True
    except:
        print('error when saving art')
        return False

def getArt(eachPage):
    try:
        html = url_open(eachPage).decode('ISO-8859-1')
        print(eachPage)
        imgLine = re.findall(r'''<div id="main-frame-info">[\s\S]+<img src="http.+"''',html)[0]
        artAddrs=re.findall('''<img src="http.+\.jpg" border=|<img src="http.+\.JPG" border=|<img src="http.+\.tif" border=|<img src="http.+\.bmp" border=|<img src="http.+\.png" border=''',imgLine)[0]
        artAddrs=artAddrs.replace('''<img src="''',"")
        artAddrs=artAddrs.replace('''" border=''',"")
        return artAddrs
    except:
        print('error when resolving art')
        
def getArtPages(mainUrl):
    try:
        artPages = {}
        html=url_open(mainUrl).decode('ISO-8859-1')
        addr = re.findall('''showthread\.php\?f=121&.+t=\d+">.+,.+\(\dD\)''',html)
        matchName = re.compile('>.+,.+\(\dD\)')
        matchToRemove = re.compile("s=.+&amp;")
        for i in addr:
            filename=matchName.search(i).group().replace(">","")
            toRemove=matchToRemove.search(i).group()
            i=i.replace(toRemove,"")
            a=i.replace(filename,"")
            print(a)
            artPages['http://forums.cgsociety.org/'+str(a)]=filename
        return artPages
    except:
        print('error when resolving pages')
    
def downloadPic(folder, startPage, endpage):
    imgNum = 1
    os.chdir(folder)
    for i in list(range(startPage,endpage+1)):
        pageNum=i
        mainUrl = "http://forums.cgsociety.org/forumdisplay.php?f=121&page=%d&sort=dateline&order=&pp=25&daysprune=-1"%(pageNum)
        print('downloading from page %s'%(str(pageNum)))
        try:
            artPages = getArtPages(mainUrl)
            for eachPage in artPages.keys():
                artAddrs = getArt(eachPage)
                result=saveArt(folder,pageNum,artAddrs,filename=artPages[eachPage])
                if result==True:
                    print ('finished saving %d images in %s \n'%(imgNum, folder))
                    imgNum+=1
                else:
                    print('failed to save art')
        except:
            print("error running downloadPic")
        time.sleep(0.2)


if __name__ == '__main__':
    folder=r"/prod/kfpdr/work/surfacing/ldong/cgsociety"
    startPage = 1
    endpage = 1
    downloadPic(folder, startPage, endpage)
