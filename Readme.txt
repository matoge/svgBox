svgBox version 1.0

Author: funaya@gmail.com
Last Update: 2011/9/1

svgBox is a python script that generates codes from freely drawn scalable vector graphics drawings for constructing "ragdolls" in NAIST ballpool. This document describes how to design ragdoll using Inkscape and edit XML file to add some parameters for physics library "Box2D." 


1. Usage

python svgBox.py <function name (name of ragdoll)>

2. File Structure

svgBox generates header files that define ragdolls with Box2D codes: some kinds of shapes, and joints with physical parameters such as restitution. One header file consists of only one inline function whose name is determined in the python run.

3. Ragdoll Design


All what you have to do is free designing ragdoll parts with predefined names and define joints that connect those parts. The names such as "ltheigh" or "larm" should not be chagnged because those names are used in the ballpool program.

Ragdoll design is nothing more than the normal drawing process on Inkscape, except for editing process special in physics computing. For example, a simple rectangle looks like this;

<rect

       style="fill:#ff0000;fill-opacity:1;stroke:#ff0000;stroke-opacity:1"

       id="rect2985"

       width="225.71428"

       height="240"

       x="85.714287"

       y="172.36218"
>

Simply put, what svgBox do is just converting this xml tag into the following "Box2D" program written in cpp codes;

>|cpp|

b2Vec2 lforearm_vertices[4];
lforearm_vertices[0].Set(10.6068927282f, 7.96176074876f);
lforearm_vertices[1].Set(10.1286807852f, 8.04095758967f);
lforearm_vertices[2].Set(10.1354412088f, 5.74478818543f);
lforearm_vertices[3].Set(10.5937573892f, 5.7534803591f);
b2PolygonShape lforearm_polygon;
lforearm_polygon.Set(lforearm_vertices, 4);

||<

As for joints, we have to put a bit modification on the XML tags using the XML editor in Inkscape: bodyA, bodyB, and joint. the bodyA and bodyB items determineswhich bodis the joint is connected to, whereas the joint item specifies joint types which is defined in the Box2D library. A resulting code would look like;

<path
     bodyB="lleg"
     bodyA="ltheigh"
     joint="b2RevoluteJoint"
     inkscape:connector-curvature="0"
     id="lknee"
     d="m 18.133622,162.74998 1.4386,0"
     style="fill:none;stroke:#000000;stroke-width:0.2;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none" /> 

In this case, the joint connects "lleg" and "ltheigh" as "bsRevoluteJoint."