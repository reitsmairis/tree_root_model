#############################################################################
# Code for converting the cylinder measures to CityJSON objects 
#############################################################################

import json
import numpy as np
import math


def to_cityJSON(radius_list, ground_level_list, groundwater_level_list, rd_x_list, rd_y_list, number_list, vertices, ambition, area, model, y, main_area):
    open('output/{}/{}/{}/{}/json_{}.city.json'.format(main_area, model, ambition, y, area), 'w') 
    f = open('output/{}/{}/{}/{}/json_{}.city.json'.format(main_area, model, ambition, y, area), 'a')
    f.write("{\"type\": \"CityJSON\", \"version\": \"1.0\", \"metadata\": {}, \"CityObjects\":")
    f.write("{")

    # for testing and checking if file ends
    totalTrees = len(number_list)
    currentTree = 0
    maxTrees = 0 

    # list for remembering the cylinder structures
    total_points = []

    # determine transform
    scale = [0.01, 0.01, 1]
    translate = [108000, 476000, 0]

    # determine vertice spread
    points_on_circle = int(vertices / 2)
    angle = 2 * np.pi / points_on_circle

    # add tiny height difference for countering z-fighting 
    if ambition == 'optimal':
        factor = 0.
    if ambition == 'reasonable':
        factor = 0.01
    if ambition == 'marginal':
        factor = 0.02

    # loop throug the rootvolume of every tree
    for count, r in enumerate(radius_list):

        if math.isnan(r):
            r = 0

        # retrieve parameters for tree
        ground_level = ground_level_list[count]
        groundwater_level = groundwater_level_list[count]
        rd_x = rd_x_list[count]
        rd_y = rd_y_list[count]
        number = number_list[count]

        # create the points of a cylinder
        points = []
        lower_points = []
        for i in range(points_on_circle):
            x = rd_x + r * np.cos(i * angle)
            y = rd_y + r * np.sin(i * angle)
            x_t = (x-translate[0]) / scale[0]
            y_t = (y-translate[1]) / scale[1]
            points.append([int(x_t), int(y_t), ground_level + factor])
            lower_points.append([int(x_t), int(y_t), groundwater_level - factor])

        # store cylinder points
        points.extend(lower_points)
        total_points.extend(points)

        # determine boundaries (polygons) for a cylinder
        boundaries = []
        add = count*vertices # for matching the boundaries to the correct vertices 
        boundaries.append([list(range(0 + add, points_on_circle + add))]) # upper polygon
        boundaries.append([list(range(vertices-1 + add, points_on_circle-1 + add, -1))]) # lower polygon

        # append side polygons
        for i in range(points_on_circle-1):
            boundaries.append([[i+add, i+add+points_on_circle, i+add+points_on_circle+1, i+add+1]])

        # append polygon connecting first and last points
        boundaries.append([[points_on_circle-1 + add, vertices-1 + add, points_on_circle + add, 0 + add]])
        #total_boundaries.append(boundaries)

        # include boundaries of a cylinder in CityJSON
        f.write("\"" + "id-{}_{}".format(number, ambition) + "\":{")
        f.write("\"type\":\"SolitaryVegetationObject\",")
        f.write("\"geometry\": [{") #geometry start
        f.write("\"boundaries\":" + str(boundaries) + ",")
        f.write("\"lod\":1,")
        f.write("\"type\":\"MultiSurface\"")
        f.write("}]") #geometry end
        f.write("}")

        currentTree +=1

        # end file properly
        if maxTrees != 0 and (currentTree >= maxTrees):
            break
        if(currentTree < totalTrees):
            f.write(",")

    f.write("},")

    # append vertices to CityJSON
    f.write("\"transform\":{\"scale\":" + str(scale) + ", \"translate\":" + str(translate)+ "}" + ",")
    f.write("\"vertices\":" + str(total_points))  
    f.write("}")
    f.close()

    return 
