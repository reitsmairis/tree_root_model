import json
import numpy as np

def to_cityJSON(radius_list, ground_level_list, groundwater_level_list, rd_x_list, rd_y_list, number_list, vertices, ambition):

    total_points = []
    total_boundaries = []
    points_on_circle = int(vertices / 2)
    angle = 2 * np.pi / points_on_circle

    city_json = {
        "type": "CityJSON",
        "version": "1.1",
        "CityObjects": {},
        "vertices": []
    }

    # add little bit of height difference, otherwise weird visual effects will come in
    if ambition == 'optimal':
        factor = 0.
    if ambition == 'reasonable':
        factor = 0.01
    if ambition == 'marginal':
        factor = 0.02

    for count, r in enumerate(radius_list):
        ground_level = ground_level_list[count]
        groundwater_level = groundwater_level_list[count]
        rd_x = rd_x_list[count]
        rd_y = rd_y_list[count]
        number = number_list[count]

        # points
        points = []
        lower_points = []
        for i in range(points_on_circle):
            x = rd_x + r * np.cos(i * angle)
            y = rd_y + r * np.sin(i * angle)
            points.append([x, y, ground_level + factor])
            lower_points.append([x, y, groundwater_level - factor])

        points.extend(lower_points)
        total_points.extend(points)

        # boundaries
        boundaries = []
        add = count*vertices
        boundaries.append([list(range(0 + add, points_on_circle + add))]) # upper polygon
        boundaries.append([list(range(vertices-1 + add, points_on_circle-1 + add, -1))]) # lower polygon

        # append side boundaries
        for i in range(points_on_circle-1):
            boundaries.append([[i+add, i+add+points_on_circle, i+add+points_on_circle+1, i+add+1]])

        # append boundary connecting first and last point
        boundaries.append([[points_on_circle-1 + add, vertices-1 + add, points_on_circle + add, 0 + add]])
        total_boundaries.append(boundaries)

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
                    "lod": "1",
                    "type": "MultiSurface"
                }
            ]
        }


    city_json["vertices"] = total_points

    return city_json