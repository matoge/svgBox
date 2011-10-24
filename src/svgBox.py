from BeautifulSoup import BeautifulStoneSoup
import math
import re
import struct

BULLET = "false"
DENSITY = 1.0
FRICTION = 0.2
RES = 0.4
L_DAMPING = 0.3
A_DAMPING = 0.3

#OBJECT_NAME = "ROBOT"
## constants to generate box2d codes
#B2Width = 4.0 # object width in box2d's world
#B2Position = [10.0,0.0] # the ground level
#DENSITY = 1000.0
#L_DAMPING = 0.7
#A_DAMPING = 0.6
#B2World = "m_world" # variable name
#B2BodyListName = "bodylist"
#B2GROUP = "-1"
#B2BODYTYPE = "b2_dynamicBody"
#
#xml = open("robot_stand.svg").read()
##output = "D:/Documents and Settings/Administrator/My Documents/hiroyuki-fn/Dropbox/Dropbox/projects/vBallpool/vBallpool/robot.h"
##output = "C:/Users/funa7/Dropbox/projects/vBallpool/vBallpool/human.h"
#output = "C:/Users/funa7/Dropbox/projects/vBallpool-4K/vBallpool/robot.h"

OBJECT_NAME = "TITLE"
##  constants to generate box2d codes
B2Width = 32.0 # object width in box2d's world
B2Position = [-14.0,8.0] # the ground level
B2World = "m_world" # variable name
B2BodyListName = "bodylist"
B2UDATALISTNAME = "title_udatalist"
B2GROUP = "0"
B2BODYTYPE = "b2_dynamicBody"

xml = open("problem7.svg").read()
output = "C:/Users/hiroyuki-fn/Dropbox/projects/vBallpool-4K/vBallpool/problem7.h"


#
import sys
sys.stdout = open(output, "w")
##
## Box2d Rectangle Shapes
##

soup = BeautifulStoneSoup(xml)

# Get the whole width and height
result = soup("svg")
hwidth = float(result[0]["width"])
hheight = float(result[0]["height"])
scale = B2Width/hwidth

# body list to store all the pointers to bodies
print "vector<b2Body*> {0};".format(B2BodyListName)

#
# Draw Polygon
#
result = soup('path')

for r in result:
    # pass if joint, which must be created last
    if r.has_key('joint'):
        continue
    if r.has_key('sodipodi:type'):
        if r['sodipodi:type']=="arc":
            continue

    id=r['id']
    # the original points
    pol_exp = re.compile('[0-9.e\-]+,[0-9.e\-]+')
    pol_ma = re.findall(pol_exp,r['d'])
    pol_vnumber = len(pol_ma)
    # transforms
    pol_tr_point = [0.0, 0.0]
    if r.has_key('transform'):
        pol_transform = r['transform']
        pt= re.findall(pol_exp,pol_transform)[0]
        pol_tr_point[0] = float(re.split(",",pt)[0])
        pol_tr_point[1] = float(re.split(",",pt)[1])
    #print "POL", pol_tr_point

    # relative to absolute
    pol_pointlist = []
    pol_x=pol_tr_point[0]
    pol_y=pol_tr_point[1]
    for i, pol_point in enumerate(pol_ma):
        pol_x += float(re.split(",",pol_point)[0])
        pol_y += float(re.split(",",pol_point)[1])
        pol_pointlist.append([pol_x,pol_y])

    pol_pointlist.reverse() # Counter Clockwise in box2d world


    # start making polygon
    #print "{"
    print "//\n//{0}\n//".format(id)
    print "b2Vec2 {0}_vertices[{1}];".format(id,pol_vnumber)
    for i, p in enumerate(pol_pointlist):
        pol_x2 = p[0]
        pol_y2 = p[1]
        print "{0}_vertices[{1}].Set({2}f, {3}f);".format(id,i,pol_x2*scale + B2Position[0],(hheight-pol_y2)*scale + B2Position[1])
        #print pol_x2*scale,(hheight-pol_y2)*scale

    print "b2PolygonShape {0}_polygon;".format(id)
    print "{0}_polygon.Set({0}_vertices, {1});".format(id,pol_vnumber)
    print ""
    print "b2FixtureDef {0}_triangleShapeDef;".format(id)
    print "{0}_triangleShapeDef.shape = &{0}_polygon;".format(id)
    print "{0}_triangleShapeDef.density = {1}f;".format(id,DENSITY)
    print "{0}_triangleShapeDef.restitution = 0.0f;".format(id)
    print "{0}_triangleShapeDef.friction = 10.0f;".format(id)
    print ""
    print "{0}_triangleShapeDef.filter.groupIndex = {1};".format(id,B2GROUP)
    print ""
    #Bodydef
    print "b2BodyDef {0}_triangleBodyDef;".format(id)
    print "{0}_triangleBodyDef.type = {1};".format(id, B2BODYTYPE)
    print "{0}_triangleBodyDef.bullet = {1};".format(id,BULLET)
    print "{0}_triangleBodyDef.linearDamping = {1}f;".format(id,L_DAMPING)
    print "{0}_triangleBodyDef.angularDamping = {1}f;".format(id,A_DAMPING)

    print "{0}_triangleBodyDef.position.Set(-0.0f, 0.0f);".format(id)
    print ""
    print "b2Body* {0}_body = m_world->CreateBody(&{0}_triangleBodyDef);".format(id)
    print "{0}_body->CreateFixture(&{0}_triangleShapeDef);".format(id)
    print "{0}.push_back({1}_body);".format(B2BodyListName,id)
    #print "}"


    # User Data
    # color
    print "uData* {0}_ud = new uData();".format(id)
    print "{0}_ud->name = \"{1}\";".format(id,OBJECT_NAME)
    if r.has_key('style'):
        styls = r['style'].split(";")
        for st in styls:
            if st.split(":")[0] == "fill":
                if st.split(":")[1] != "none":
                    rgb = struct.unpack('BBB',st[6:].decode('hex'))
                    print "{0}_ud->fill.Set(float({1})/255,float({2})/255,float({3})/255);".format(id, rgb[0],rgb[1],rgb[2])
                else: #white
                    print "{0}_ud->fill.Set(1.0f,1.0f,1.0f);".format(id)
            if st.split(":")[0] == "stroke":
                if st.split(":")[1] != "none":
                    rgb = struct.unpack('BBB',st[8:].decode('hex'))
                    print "{0}_ud->stroke.Set(float({1})/255,float({2})/255,float({3})/255);".format(id, rgb[0],rgb[1],rgb[2])
                else: #black
                    print "{0}_ud->stroke.Set(1.0f,1.0f,1.0f);".format(id)
            if st.split(":")[0] == "stroke-width":
                print "{0}_ud->strokewidth={1}f;".format(id,st.split(":")[1])
    print "{0}_body->SetUserData({0}_ud);".format(id)



#
# Simple rectangle
#
result = soup.findAll('rect')
for r in result:
    #print r
    #print type(r)
    width = float(r['width'])
    height = float(r['height'])
    x = float(r['x'])
    y = float(r['y'])
    id = r['id']

    angle = 0.0
    m22 = [1,0,0,1]
    # transform is described as an affine matrix with parallel transition
    if r.has_key('transform'):
        exp1 = re.compile('matrix\((.*),(.*),(.*),(.*),.*,.*\)')
        # exp2 = re.compile('transform\((.*),(.*)\)')
        m = re.match(exp1,r['transform'])
        m22 = [float(m.group(1)),float(m.group(2)),float(m.group(3)),float(m.group(4))]
        angle = math.asin(m22[1])

    # center point
    ## center point in inclined coordinate
    cx2 = x + width/2
    cy2 = y + height/2
    centerx = ( m22[0] * cx2 - m22[1] * cy2 ) * scale
    centery = ( - m22[2] * cx2 + m22[3] * cy2 )
    ## Box2d and svg is upside down
    centery = (hheight - centery) * scale

    # Start creating rectangle
    #print "{"
    print "\n//\n//{0}\n//".format(id)
    print "b2BodyDef {0}_bdef;".format(id)
    print "{0}_bdef.type = {1};".format(id,B2BODYTYPE)
    print "{0}_bdef.bullet = {1};".format(id,BULLET)
    print "{0}_bdef.position.Set({1}f,{2}f);".format(id,centerx+B2Position[0],centery+B2Position[1])
    print "{0}_bdef.angle={1}f;".format(id,-1*angle)
    print "{0}_bdef.linearDamping = {1}f;".format(id,L_DAMPING)
    print "{0}_bdef.angularDamping ={1}f;".format(id,A_DAMPING)
    print "b2Body* {0}_body = m_world->CreateBody(&{0}_bdef);".format(id)
    print ""
    print "b2PolygonShape {0}_ps;".format(id)
    print "{0}_ps.SetAsBox({1}f, {2}f);".format(id,width/2*scale,height/2*scale)
    print ""
    print "b2FixtureDef {0}_fdef;".format(id)
    print "{0}_fdef.shape = &{0}_ps;".format(id)
    print ""
    print "{0}_fdef.density = {1}f;".format(id,DENSITY)
    print "{0}_fdef.friction = {1}f;".format(id,FRICTION)
    print "{0}_fdef.restitution = {1}f;".format(id, RES)
    print "{0}_fdef.filter.groupIndex = {1};".format(id,B2GROUP)
    print ""
    # if r.has_key('parent')
    print "{0}_body->CreateFixture(&{0}_fdef);".format(id)
    print "{0}.push_back({1}_body);".format(B2BodyListName,id)
    #print "}"


    # User Data
    # color
    print "uData* {0}_ud = new uData();".format(id)
    print "{0}_ud->name = \"{1}\";".format(id,OBJECT_NAME)
    if r.has_key('style'):
        styls = r['style'].split(";")
        for st in styls:
            if st.split(":")[0] == "fill":
                if st.split(":")[1] != "none":
                    rgb = struct.unpack('BBB',st[6:].decode('hex'))
                    print "{0}_ud->fill.Set(float({1})/255,float({2})/255,float({3})/255);".format(id, rgb[0],rgb[1],rgb[2])
                else: #white
                    print "{0}_ud->fill.Set(1.0f,1.0f,1.0f);".format(id)
            if st.split(":")[0] == "stroke":
                if st.split(":")[1] != "none":
                    rgb = struct.unpack('BBB',st[8:].decode('hex'))
                    print "{0}_ud->stroke.Set(float({1})/255,float({2})/255,float({3})/255);".format(id, rgb[0],rgb[1],rgb[2])
                else: #black
                    print "{0}_ud->stroke.Set(1.0f,1.0f,1.0f);".format(id)
            if st.split(":")[0] == "stroke-width":
                print "{0}_ud->strokewidth={1}f;".format(id,st.split(":")[1])
    print "{0}_body->SetUserData({0}_ud);".format(id)

#
# Circle
#

result = soup.findAll('path', {'sodipodi:type':"arc"} )
result.reverse()
for r in result:
    #print r
    #print type(r)
    radius = float(r['sodipodi:rx']) * scale
    x = float(r['sodipodi:cx'])
    y = float(r['sodipodi:cy'])
    id = r['id']
    # center point
    ## center point in inclined coordinate
    if r.has_key('transform'):
        exp1 = re.compile('translate\((.*),(.*)\)')
        # exp2 = re.compile('transform\((.*),(.*)\)')
        m = re.match(exp1,r['transform'])
        x += float(m.group(1))
        y += float(m.group(2))

    # center point
    ## center point in inclined coordinate
    cx = ( x ) * scale
    cy = ( hheight - y ) * scale

    # Start creating rectangle
    #print "{"
    print "\n//\n//{0}\n//".format(id)
    print "b2BodyDef {0}_bdef;".format(id)
    print "{0}_bdef.type = {1};".format(id, B2BODYTYPE)
    print "{0}_bdef.bullet = {1};".format(id,BULLET)
    print "{0}_bdef.position.Set({1}f,{2}f);".format(id,cx+B2Position[0],cy+B2Position[1])
    print "{0}_bdef.linearDamping = {1}f;".format(id,L_DAMPING)
    print "{0}_bdef.angularDamping ={1}f;".format(id,A_DAMPING)
    print "b2Body* {0}_body = m_world->CreateBody(&{0}_bdef);".format(id)
    print ""
    print "b2CircleShape {0}_s;".format(id)
    print "{0}_s.m_radius={1}f;".format(id,radius)
    print ""
    print "b2FixtureDef {0}_fdef;".format(id)
    print "{0}_fdef.shape = &{0}_s;".format(id)
    print ""
    print "{0}_fdef.density = {1}f;".format(id,DENSITY)
    print "{0}_fdef.friction = 0.1f;".format(id)
    print "{0}_fdef.restitution = 0.8f;".format(id)
    print "{0}_fdef.filter.groupIndex = {1};".format(id,B2GROUP)
    print ""
    # if r.has_key('parent')
    print "{0}_body->CreateFixture(&{0}_fdef);".format(id)
    print "{0}.push_back({1}_body);".format(B2BodyListName,id)

    # User Data
    # color
    print "uData* {0}_ud = new uData();".format(id)
    print "{0}_ud->name = \"{1}\";".format(id,OBJECT_NAME)
    if r.has_key('style'):
        styls = r['style'].split(";")
        for st in styls:
            if st.split(":")[0] == "fill":
                if st.split(":")[1] != "none":
                    rgb = struct.unpack('BBB',st[6:].decode('hex'))
                    print "{0}_ud->fill.Set(float({1})/255,float({2})/255,float({3})/255);".format(id, rgb[0],rgb[1],rgb[2])
                else: #white
                    print "{0}_ud->fill.Set(1.0f,1.0f,1.0f);".format(id)
            if st.split(":")[0] == "stroke":
                if st.split(":")[1] != "none":
                    rgb = struct.unpack('BBB',st[8:].decode('hex'))
                    print "{0}_ud->stroke.Set(float({1})/255,float({2})/255,float({3})/255);".format(id, rgb[0],rgb[1],rgb[2])
                else: #black
                    print "{0}_ud->stroke.Set(1.0f,1.0f,1.0f);".format(id)
            if st.split(":")[0] == "stroke-width":
                print "{0}_ud->strokewidth={1}f;".format(id,st.split(":")[1])
    print "{0}_body->SetUserData({0}_ud);".format(id)


#
# B2RevoluteJoints
#
result = soup('path', joint="b2RevoluteJoint")

for r in result:

    # the original points
    pol_exp = re.compile('[0-9.e\-]+,[0-9.e\-]+')
    pol_ma = re.findall(pol_exp,r['d'])
    pol_vnumber = len(pol_ma)
    # transforms
    pol_tr_point = [0.0, 0.0]
    if r.has_key('transform'):
        pol_transform = r['transform']
        pt= re.findall(pol_exp,pol_transform)[0]
        pol_tr_point[0] = float(re.split(",",pt)[0])
        pol_tr_point[1] = float(re.split(",",pt)[1])
    #print "POL", pol_tr_point

    # relative to absolute
    pol_pointlist = []
    pol_x=pol_tr_point[0]
    pol_y=pol_tr_point[1]
    for i, pol_point in enumerate(pol_ma):
        pol_x += float(re.split(",",pol_point)[0])
        pol_y += float(re.split(",",pol_point)[1])
        pol_pointlist.append([pol_x,pol_y])

    #print "{"
    print "//{0}".format(r['id'])
    print "b2RevoluteJointDef {0}_rjd;".format(r['id'])
    print ""
    print "{0}_rjd.Initialize({1}_body, {2}_body, b2Vec2({3}f, {4}f));".format(r['id'],r['bodya'], r['bodyb'], pol_pointlist[0][0]*scale+B2Position[0], (hheight-pol_pointlist[0][1])*scale+B2Position[1])
    print "{0}_rjd.motorSpeed = 100.0f * b2_pi;".format(r['id'])
    print "{0}_rjd.maxMotorTorque = 10.0f;".format(r['id'])
    print "{0}_rjd.enableMotor = false;".format(r['id'])
    print "{0}_rjd.lowerAngle = -0.5f * b2_pi;".format(r['id'])
    print "{0}_rjd.upperAngle = 0.5f * b2_pi;".format(r['id'])
    print "{0}_rjd.enableLimit = false;".format(r['id'])
    print "{0}_rjd.collideConnected = false;".format(r['id'])
    print ""
    print "b2RevoluteJoint* {0}_joint = (b2RevoluteJoint*)m_world->CreateJoint(&{0}_rjd);".format(r['id'])
    print ""
    #print "}"



#
# B2WeldJoints
#
result = soup('path', joint="b2WeldJoint")

for r in result:

    # the original points
    pol_exp = re.compile('[0-9.e\-]+,[0-9.e\-]+')
    pol_ma = re.findall(pol_exp,r['d'])
    pol_vnumber = len(pol_ma)
    # transforms
    pol_tr_point = [0.0, 0.0]
    if r.has_key('transform'):
        pol_transform = r['transform']
        pt= re.findall(pol_exp,pol_transform)[0]
        pol_tr_point[0] = float(re.split(",",pt)[0])
        pol_tr_point[1] = float(re.split(",",pt)[1])
    #print "POL", pol_tr_point

    # relative to absolute
    pol_pointlist = []
    pol_x=pol_tr_point[0]
    pol_y=pol_tr_point[1]
    for i, pol_point in enumerate(pol_ma):
        pol_x += float(re.split(",",pol_point)[0])
        pol_y += float(re.split(",",pol_point)[1])
        pol_pointlist.append([pol_x,pol_y])

    #print "{"
    print "//{0}".format(r['id'])
    print "b2WeldJointDef {0}_wjd;".format(r['id'])
    print ""
    print "{0}_wjd.Initialize({1}_body, {2}_body, b2Vec2({3}f, {4}f));".format(r['id'],r['bodya'], r['bodyb'], pol_pointlist[0][0]*scale+B2Position[0], (hheight-pol_pointlist[0][1])*scale+B2Position[1])
    print ""
    print "b2WeldJoint* {0}_joint = (b2WeldJoint*)m_world->CreateJoint(&{0}_wjd);".format(r['id'])
    print ""
    #print "}"



#
# B2DistantJoints
#
result = soup('path', joint="b2DistanceJoint")

for r in result:

    # the original points
    pol_exp = re.compile('[0-9.e\-]+,[0-9.e\-]+')
    pol_ma = re.findall(pol_exp,r['d'])
    pol_vnumber = len(pol_ma)
    # transforms
    pol_tr_point = [0.0, 0.0]
    if r.has_key('transform'):
        pol_transform = r['transform']
        pt= re.findall(pol_exp,pol_transform)[0]
        pol_tr_point[0] = float(re.split(",",pt)[0])
        pol_tr_point[1] = float(re.split(",",pt)[1])
    #print "POL", pol_tr_point

    # relative to absolute
    pol_pointlist = []
    pol_x=pol_tr_point[0]
    pol_y=pol_tr_point[1]
    for i, pol_point in enumerate(pol_ma):
        pol_x += float(re.split(",",pol_point)[0])
        pol_y += float(re.split(",",pol_point)[1])
        pol_pointlist.append([pol_x,pol_y])

    #print "{"
    print "//{0}".format(r['id'])
    print "b2DistanceJointDef {0}_djd;".format(r['id'])
    print ""
    print "{0}_djd.Initialize({1}_body, {2}_body, b2Vec2({3}f, {4}f), b2Vec2({5}f, {6}f));".format(r['id'],r['bodya'], r['bodyb'], pol_pointlist[0][0]*scale+B2Position[0], (hheight-pol_pointlist[0][1])*scale+B2Position[1], pol_pointlist[1][0]*scale+B2Position[0], (hheight-pol_pointlist[1][1])*scale+B2Position[1])
    print ""
    print "b2DistanceJoint* {0}_joint = (b2DistanceJoint*)m_world->CreateJoint(&{0}_djd);".format(r['id'])
    print ""
    #print "}"

