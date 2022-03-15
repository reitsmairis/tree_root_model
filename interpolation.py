################################
# from: https://github.com/marcomusy/vedo/blob/master/examples/basic/delaunay2d.py
# and: https://stackoverflow.com/questions/57058089/how-to-use-vtkobbtree-and-intersectwithline-to-find-the-intersection-of-a-line-a
################################################

from vedo import *
import numpy as np


def interpolate(points):

    # create points object
    pts = Points(points, r=6)

    # do 2D Delauny interpolation
    mesh = delaunay2D(pts, mode='xy')

    return mesh

def intersect(mesh, x, y):

    large_number = 100 # used for intersection, groundwater will not be outside of - and + this number

    # create line
    p0 = (x, y, -large_number)
    p1 = (x, y, large_number)

    # calculate intersection point
    intersect_points = mesh.intersectWithLine(p0, p1)
    intersect_coord = intersect_points[0]
    print('the groundwater level at coordinate ({},{}) is {}'.format(intersect_coord[0] ,intersect_coord[1], intersect_coord[2]))

    return intersect_coord

points = np.load('grondwater/GHG_values_Sarphati.npy')
print(points)
mesh = interpolate(points)
mesh.write('Sarphati_mesh.vtk')
mesh_v = mesh.addElevationScalars(lowPoint=(0,0,-3), highPoint=(0,0,1), vrange=(-1,1))
#mesh_v.cmap('hot')
show(Points(points, r=6), mesh_v, bg="Mint", axes=1).close()
#x, y = 121670, 486887
#intersect(mesh, x, y)

# visualize, but difference is not big enough to visualize
# pts = Points(points, r=6).c('blue3')
# mesh = delaunay2D(pts, mode='xy').c('w').lc('black').lw(1)
# mesh_v = mesh.addElevationScalars(lowPoint=(0,0,-0.6), highPoint=(0,0,0.3), vrange=(-0.6,0.3))
# mesh_v.cmap('hot')
# mesh_v.addScalarBar('groundwater level (m)', pos=(0.65, 0.4))
# show(pts, mesh_v, bg="Mint", axes=1).close()

# Old code with visualization::
#
# # example points
# gridSize = 10
# points = []
# for x in range(gridSize):
#     for y in range(gridSize):
#         points.append([x, y, int((x + y) / (y + 1))])
# pts = Points(points, r=6).c('blue3')
#
#
# # do 2D Delauny interpolation
# mesh = delaunay2D(points, mode='xy').c('w').lc('o').lw(1)
#
# # example line
# p0 = (8.3, 1.9, -100)
# p1 = (8.3, 1.9, 100)
#
# # calculate intersection point
# intersect_points = mesh.intersectWithLine(p0, p1)
# intersect_coord = intersect_points[0]
# print(intersect_coord)
# print('the groundwater level at coordinate ({},{}) is {}'.format(intersect_coord[0] ,intersect_coord[1], intersect_coord[2]))
#
# # visualize
# show(pts, mesh, Points(intersect_points, r=10).c('r'), __doc__, bg="Mint").close()
