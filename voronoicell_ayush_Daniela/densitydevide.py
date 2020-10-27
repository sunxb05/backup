import numpy as np
from scm.plams import *
from scipy.spatial import cKDTree
#import matplotlib.pyplot as plt
import os.path
#from mayavi import mlab
unit = 0.5291 # converting bohr to angstrom
def vis_density (density, grid):
   x = []; y = []; z = []
   for i in range(0, len(grid)):
      x.append(grid[i][0])
      y.append(grid[i][1])
      z.append(grid[i][2])
   print(len(z))
   mlab.points3d(x, y, z, density)
   mlab.show()
   return
def distance(v1,v2):
   return np.sqrt(np.dot(v1 - v2, v1 - v2))
def voronoi_charges(voronoi_matrix, density, weight):
   return density @ (voronoi_matrix*weight)
# def voronoi_partition(atom_coord, grid, nx, ny, nz, natoms):
#    voronoi_matrix = np.empty((nx*ny*nz, natoms))  # nx*ny*nz  total dimension
#    for i,j in enumerate(atom_coord):
#       voronoi_matrix[:, i] =  np.stack(np.apply_along_axis(lambda v: distance(v, j), axis=1, arr=grid))
#    return (voronoi_matrix == voronoi_matrix.min(axis=1)[:,None]).astype(float)
def voronoi_partition(atom_coord, grid, nx, ny, nz, natoms):
   voronoi_matrix = np.empty((nx*ny*nz, natoms))
   voronoi_kdtree = cKDTree(atom_coord)
   grid_point_dist, atom_point_regions = voronoi_kdtree.query(grid, k=1)
   for i,j in enumerate(atom_point_regions):
      voronoi_matrix[i,j] = 1
   return voronoi_matrix
def grid_gen(start_coord, length, nx, ny, nz):
   length = length*unit  # outermost loop is z and innermost is x
   xs     = np.linspace(start_coord[0], start_coord[0] + nx*length, num = nx, endpoint = False)
   ys     = np.linspace(start_coord[1], start_coord[1] + ny*length, num = ny, endpoint = False)
   zs     = np.linspace(start_coord[2], start_coord[2] + nz*length, num = nz, endpoint = False)
   grid   = np.stack(np.meshgrid(zs, ys, xs, indexing = 'ij'), axis = 3).reshape(nx*ny*nz, 3)
   return grid[:,[2,1,0]]
def main():
   mykf_frag1 = KFFile('frag1')
   mykf_frag2 = KFFile('frag2')
   mol = Molecule('ci.xyz')
   density_frag1      = mykf_frag1['SCF_A%8']
   density_frag2      = mykf_frag2['SCF_A%31']
   overlap_density    = [a * b for a,b in zip(density_frag1, density_frag2)]
   nx                 = mykf_frag1["Grid%nr of points x"]
   ny                 = mykf_frag1["Grid%nr of points y"]
   nz                 = mykf_frag1["Grid%nr of points z"]
   start_coord        = [i*unit for i in mykf_frag1['Grid%Start_point']]
   atom_coord = [atom.coords for atom in mol.atoms]
   atom_coord = [list(x) for x in atom_coord]
   coordinates        = (np.array(atom_coord))*(unit) # KFFile changes the units to Bohr
   natoms             = len(coordinates)
   x_vector           = mykf_frag1['Grid%x-vector']
   length             = x_vector[0]
   weight             = length**3
   at_num = [atom.atnum for atom in mol.atoms]
   print ('densities are = {} {} {}'.format(sum(overlap_density)*weight, sum(density_frag1)*weight, sum(density_frag2)*weight))
   grid = grid_gen(start_coord,length, nx, ny, nz) # generating the grid
   if os.path.isfile("partition-test.npy"):
      voronoi_matrix = np.load("partition-test.npy") #calculating the voronoi partition
   else:
      voronoi_matrix = voronoi_partition(coordinates, grid, nx, ny, nz, natoms)
      np.save("partition-test", voronoi_matrix)
   charges = voronoi_charges(voronoi_matrix, overlap_density, weight) #calculating the voronoi charges from the overlap density
   #for i in range(natoms):
      #print ("{} {}". format(labels[i], coordinates[i]))
   for i in range(natoms):
      print ("at_num = {} & voronoi_charge = {:.4}".format(at_num[i], charges[i]))
   #vis_density (overlap_density, grid)
if __name__ == "__main__":
   main()
