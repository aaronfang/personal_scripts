# rename selected geos to fit the pattern as perfix_###_sufix
perfix = 'M_'
sufix = '_geo'
curSel = cmds.ls(sl=1,fl=1)
for geo in curSel:
	if geo.split('_')[0]=='M'or geo.split('_')[0]=='L'or geo.split('_')[0]=='R' and geo.split('_')[-1]=='geo':
		midNm = geo.replace(geo[:2],'').replace(geo[-4:],'')
		cmds.rename(geo,perfix+midNm+sufix)
	else: cmds.rename(geo,perfix+geo+sufix)
