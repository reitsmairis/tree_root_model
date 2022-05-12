#############################################################################
# Code for converting the cylinder measures to CityJSON objects 
#############################################################################

import json
import numpy as np
import math


def to_cityJSON(radius_list, ground_level_list, groundwater_level_list, rd_x_list, rd_y_list, number_list, vertices, ambition):

    # list for remembering the cylinder structures
    total_points = []
    total_boundaries = []

    # determine vertice spread
    points_on_circle = int(vertices / 2)
    angle = 2 * np.pi / points_on_circle

    # initiate CityJSON file
    city_json = {
        "type": "CityJSON",
        "version": "1.0",
        "CityObjects": {},
        "transform": {
            "scale": [0.01, 0.01, 0.01],
            "translate": [108000, 476000, 0]
        },
        "vertices": []
    }

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
            x_t = (x-city_json["transform"]["translate"][0]) / city_json["transform"]["scale"][0]
            y_t = (y-city_json["transform"]["translate"][1]) / city_json["transform"]["scale"][1]
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
        total_boundaries.append(boundaries)

        # include boundaries of a cylinder in CityJSON
        title = "id-{}_{}".format(number, ambition)
        city_json["CityObjects"][title] = {
            "type": "SolitaryVegetationObject",
            "attributes":
            {
                "function": "something"
            },
            "geometry":
            [
                {
                    "boundaries":

                        total_boundaries[count]
                    ,
                    "lod": 1,
                    "type": "MultiSurface"
                }
            ]
        }

    # append vertices to CityJSON
    city_json["vertices"] = total_points

    return city_json
