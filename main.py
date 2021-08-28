#! /usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import division
from pathlib import Path
import os, sys, re, math, time, subprocess

# Assumes SolidPython is in site-packages or elsewhwere in sys.path
from solid import *
from solid.utils import *

SEGMENTS = 120


# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

class Pot:
    def __init__(self, sides=6, height=30, radius=60, layers=2, wall_thickness=12, roundEdges=True, leveledTop=True, overlap=1.05):
        # Properties
        self.sides = sides
        self.height = height
        self.radius = radius
        self.layers = layers
        self.wall_thickness = wall_thickness
        self.leveledTop = leveledTop
        self.overlap = overlap

        # Models / Individual pieces
        self.pieces = {}
        self.model = []

        # Block dimensions
        self.block_length = 2*radius*math.tan(math.pi/sides) # find the side length of the given polygon: a = 2r tan(π/n)
        self.block_width = wall_thickness
        self.block_height = height/layers/2
        self.interior_angle = (sides-2)*180/sides # Calculate the interior angle: ( n − 2 ) × 180 / n, where n is the number of sides

        self.vertex_len = self.determineVertex()

        # Create Pot
        self.generateFloor()
        self.generateSides()

        if roundEdges == True:
            self.roundEdges()

    def determineVertex(self):
        if self.sides == 3: # calculate vertex to vertex distance if it's a triangle
            return self.radius*2

        elif self.sides == 4: # if it's a square
            return math.sqrt(self.radius**2 + self.radius**2)

        else: # if it's any other type of normal polygon
            return math.sqrt(self.radius**2 + (self.block_length/2+(self.block_width/2*self.overlap))**2)

    # Floor
    def generateFloor(self):
        floor_distance = self.radius*2+self.block_width*2
        floor_planks = math.floor(floor_distance/self.block_width/2)
        floor_difference = floor_distance - (floor_planks*self.block_width)
        floor_plank_spacing = floor_difference*2 / floor_planks
        floor_origin = 0 - (floor_distance/2)

        floor = []

        for layer in range(2): # 2 because there are two layers to the floor
            for plank in range(floor_planks):
                if plank != 0 and plank != floor_planks-1: # skip first and last plank
                    angle = self.interior_angle-90+layer*90
                    trans_y = floor_origin+(self.block_width+floor_plank_spacing*plank)
                    trans_z = layer*self.block_height

                    cube_width = self.radius*3+(self.block_width*self.overlap)

                    floor_board = cube([cube_width, self.block_width, self.block_height], center=True)
                    floor_board = translate([0,trans_y, trans_z])(floor_board)
                    floor_board = rotate(a=angle)(floor_board)

                    floor = union()(floor,floor_board)

        #remove excess floor planks
        excess = []
        for side in range(math.ceil(self.sides)):
            excessOuter = cube([self.vertex_len*3, self.vertex_len*3, self.vertex_len*3], center=True)
            excessOuter = rotate(a=self.interior_angle)(excessOuter)

            excessInner = cube([self.radius*2+self.block_width, self.vertex_len*2, self.vertex_len*2], center=True)
            excessInner = rotate(self.interior_angle*side-90)(excessInner)

            excess = excessOuter-excessInner
            floor = floor - excess

        self.pieces['floor'] = floor
        self.model = union()(self.model,floor)

    # Walls
    def generateSides(self):
        walls = []

        for layer in range(self.layers):
            for side in range(self.sides):
                trans_y = self.radius
                trans_z = self.block_height*layer*2

                if side%2 > 0: # If side is odd
                    trans_y = self.radius*-1
                    trans_z = self.block_height*layer*2 + self.block_height

                if (layer == self.layers-1) and self.leveledTop == True: #if it's the top layer and leveledTop is true
                    trans_z = self.block_height*layer*2

                wall = cube([self.block_length+(self.block_width*self.overlap),self.block_width, self.block_height], center = True)
                wall = translate([0,trans_y, trans_z])(wall)
                wall = rotate(a=self.interior_angle*side)(wall)
                
                self.pieces[f'wall(layer_{layer}-side_{side})'] = wall
                walls = union()(walls, wall)

        self.model = union()(self.model,walls)

    def roundEdges(self):
        innerCyl = cylinder(r=self.vertex_len, h=self.height*5, center= True)
        outerCyl = cylinder(r=self.vertex_len*2, h=self.height*4, center= True)
        outerCyl = outerCyl - innerCyl
        
        for piece in self.pieces.keys():
            self.pieces[piece] -= outerCyl

        self.model -= outerCyl

    def exportPieces(self, name):
        l = len(self.pieces.keys())
        print("Exporting pieces to SCAD and STL")
        printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
        i = 0

        for piece in self.pieces.keys():
            i += 1

            model = self.pieces[piece]
            file_name = f'{piece}.scad'
            out_dir = f'{os.curdir}/{name}'
            Path(out_dir).mkdir(parents=True, exist_ok=True)

            scad_render_to_file(model, f'{out_dir}/{file_name}', file_header='$fn = %s;' % SEGMENTS, include_orig_code=False)
            subprocess.run(["openscad", "-o",  f'{out_dir}/{piece}.stl', f'{out_dir}/{file_name}'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            # Update Progress Bar
            printProgressBar(i, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
        print(f'SCAD/STL Files written to: {out_dir}')

    def exportModel(self, name):
        print("Exporting full model to SCAD and STL")
        printProgressBar(0, 1, prefix = 'Progress', suffix = 'Complete', length = 50)

        model = self.model
        file_name = f'{name}.scad'
        out_dir = f'{os.curdir}/{name}'
        Path(out_dir).mkdir(parents=True, exist_ok=True)

        scad_render_to_file(model, f'{out_dir}/{file_name}', file_header='$fn = %s;' % SEGMENTS, include_orig_code=False)
        subprocess.run(["openscad", "-o",  f'{out_dir}/{name}.stl', f'{out_dir}/{file_name}'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Update Progress Bar
        printProgressBar(1, 1, prefix = 'Progress:', suffix = 'Complete', length = 50)
        print(f'SCAD/STL Files written to: {out_dir}')


myPot = Pot()

myPot.exportPieces('HexPot')
myPot.exportModel('HexPot')