#################################################################################
# Code for interpolating the groundwater levels (GHG) to a mesh and calculating 
# the intersection of a tree location with this mesh.
################################################################################

from vedo import *
import numpy as np


def interpolate(points):
    '''Creates a mesh from 2D Delaunay triangulazition on a set of points.'''

    # create points object
    pts = Points(points, r=6)

    # do 2D Delaunay interpolation
    mesh = delaunay2D(pts, mode='xy', tol=0.005)

    return mesh


def intersect(mesh, x, y):
    '''Determines the GHG at a tree location by intersection.'''

    large_number = 100 # used for intersection, groundwater will probably not be outside of - and + this number

    # create line
    p0 = (x, y, -large_number)
    p1 = (x, y, large_number)

    # calculate intersection point
    intersect_points = mesh.intersectWithLine(p0, p1)
    intersect_coord = intersect_points[0]

    return intersect_coord


####################### main: adjust interpolation parameters ##############################

#points = np.load('grondwater/GHG_values_Amsterdam.npy') # load the GHG values

## create mesh from points
#mesh = interpolate(points)
#mesh = mesh.fillHoles()
#mesh.write('grondwater/Amsterdam_mesh.vtk') # save the mesh, choose filename

## optional code for visualising the mesh
#mesh = load('grondater/Filled_amsterdam_mesh.vtk')
#mesh_v = mesh.addElevationScalars(lowPoint=(0,0,-3), highPoint=(0,0,1), vrange=(-1,1))
#mesh_v.cmap('hot')
#(Points(area_points, r=6), mesh_v, bg="Mint", axes=1).close()

######################################################################################
