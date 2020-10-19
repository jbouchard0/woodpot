#! /usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import division
import os
import sys
import re
import math

# Assumes SolidPython is in site-packages or elsewhwere in sys.path
from solid import *
from solid.utils import *

SEGMENTS = 75

def calcDimensions(radius, height, wall_thickness, sides, layers, roundEdges, leveledTop, overlap):
    blockLength = 2*radius*math.tan(math.pi/sides)
    blockWidth = wall_thickness
    blockHeight = height/layers/2
    blockAngle = 180*(sides-2)/sides

    if sides == 3: # calculate vertex to vertex distance if it's a triangle
        VertexToVertex = radius*2

    elif sides == 4: # if it's a square
        VertexToVertex = math.sqrt(radius**2 + radius**2)

    else: # if it's any other type of normal polygon
        VertexToVertex = math.sqrt(radius**2 + (blockLength/2+(blockWidth/2*overlap))**2)

    block = []
    # pot bottom
    #planks = math.ceil(radius*2.05/wall_thickness)

    floor_distance = radius*2 + blockWidth*2
    planks = math.floor(floor_distance/blockWidth/2)
    print(planks)
    floor_difference = floor_distance - (planks*blockWidth)
    plank_spacing = floor_difference*2 / planks
    floor_origin = 0 - (floor_distance/2)
    print(plank_spacing)
    for l in range(2): # 2 sets of planks
        for p in range(planks):
            if p == 0 or p == planks-1: # skip first and last planks
                pass
            else:
                print(p)
                newSide = rotate(a=blockAngle-90+l*90)(translate([0,floor_origin+(blockWidth+plank_spacing*p),l*blockHeight])(cube([radius*3+(blockWidth*overlap),blockWidth,blockHeight], center = True)))

                block = union()(block,newSide)
    #remove excess floor planks
    
    excess = []
    for e in range(math.ceil(sides)):
        excessOuter = rotate(a=blockAngle*e)(cube([VertexToVertex*3, VertexToVertex*3, VertexToVertex*3], center=True))
        excessInner = rotate(blockAngle*e-90)(cube([radius*2+blockWidth, VertexToVertex*2, VertexToVertex*2], center=True))
        excess = excessOuter-excessInner
        block = block - excess
    
    
    for l in range(layers): # Sides of the pot
        for s in range(sides): #Generate layers
            if (l == layers-1) and leveledTop == True: #if it's the top layer and leveledTop is true
                if (s%2 == 0): # if side iter is even
                    newSide = rotate(a=blockAngle*s)(translate([0,radius,blockHeight*l*2])(cube([blockLength+(blockWidth*overlap),blockWidth,blockHeight], center = True)))
                    block = union()(block,newSide)

                elif (s%2 > 0): # else side iter is odd
                    newSide = rotate(a=blockAngle*s)(translate([0,radius*-1,blockHeight*l*2])(cube([blockLength+(blockWidth*overlap),blockWidth,blockHeight], center = True)))
                    block = union()(block,newSide)

            elif (s%2 == 0): # if side iter is even
                newSide = rotate(a=blockAngle*s)(translate([0,radius,blockHeight*l*2])(cube([blockLength+(blockWidth*overlap),blockWidth,blockHeight], center = True)))
                block = union()(block,newSide)
            elif (s%2 > 0): # else side iter is odd
                newSide = rotate(a=blockAngle*s)(translate([0,radius*-1,blockHeight*l*2+blockHeight])(cube([blockLength+(blockWidth*overlap),blockWidth,blockHeight], center = True)))
                block = union()(block,newSide)

    if roundEdges == True:
        innerCyl = cylinder(r=VertexToVertex, h=height*5, center= True)
        outerCyl = cylinder(r=VertexToVertex*2, h=height*4, center= True)
        outerCyl = outerCyl - innerCyl
        block = block - outerCyl
    return block

def assembly():
    #6 sided etsy
    #block = calcDimensions(radius=75,height=90,wall_thickness=15,sides=6,layers=5,roundEdges=True, leveledTop=False,overlap=1.05)
    #4 sided etsy
    block = calcDimensions(radius=60,height=80,wall_thickness=12,sides=4,layers=5,roundEdges=False, leveledTop=True,overlap=1.05)

    a = union()(block)

    return a

if __name__ == '__main__':
    a = assembly()
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.curdir
    file_out = os.path.join(out_dir, 'woodpot.scad')

    print("%(__file__)s: SCAD file written to: \n%(file_out)s" % vars())

    scad_render_to_file(a, file_out, file_header='$fn = %s;' % SEGMENTS, include_orig_code=True)
