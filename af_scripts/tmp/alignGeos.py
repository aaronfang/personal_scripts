import math
import maya.cmds as cmds
import numpy

def calc_angle(sx,sy,ex,ey): 
    angle=0
    y_se= ey-sy;
    x_se= ex-sx;
    if x_se==0 and y_se>0:
        angle = 360
    if x_se==0 and y_se<0:
        angle = 180
    if y_se==0 and x_se>0:
        angle = 90
    if y_se==0 and x_se<0:
        angle = 270
    if x_se>0 and y_se>0:
       angle = math.atan(x_se/y_se)*180/math.pi
    elif x_se<0 and y_se>0:
       angle = 360 + math.atan(x_se/y_se)*180/math.pi
    elif x_se<0 and y_se<0:
       angle = 180 + math.atan(x_se/y_se)*180/math.pi
    elif x_se>0 and y_se<0:
       angle = 180 + math.atan(x_se/y_se)*180/math.pi
    return angle


import maya.cmds as cmds

v1 = [10, -27, 0]
#for X axis
v2 = [1, 0, 0]

v1_u = v1 / numpy.linalg.norm(v1)
v2_u = v2 / numpy.linalg.norm(v2)

print v1_u
print v2_u

angle = numpy.arccos(numpy.dot(v1_u, v2_u))
print angle


# select 2 verts to create a 1 degree curve with a point at center.
get_verts = cmds.ls(sl=True,fl=True)
va = cmds.pointPosition(get_verts[0])
if len(get_verts) == 2:
    curve_a = cmds.curve('curve_a',d=1,p=

# get location of these 3 points. 
# calc_angle use the first and last point. 
# align the mid point in various ways.
