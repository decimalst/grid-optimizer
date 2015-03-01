from scipy.spatial import Delaunay
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
from scipy.sparse import *

#Computes the matrix edges from Triangular simplice array
def find_edges(triang):
    edges_list=list()
    temp_edges_list=list()
    #simplices is CCW points orientation
    #0->1 edge, 1->2 edge, 2->0 edge
    for simplex in triang.simplices:
        #append tuples of the points
        temp_edges_list.append((simplex[0],simplex[1]))
        temp_edges_list.append((simplex[1],simplex[2]))
        temp_edges_list.append((simplex[2],simplex[1]))
        for element in temp_edges_list:
            edges_list.append(element)
        temp_edges_list=list()
    return list(set(edges_list))

#Load all the points into a regular Python array
verts = open(r'UK_Cities_coord.txt', 'r')
firstline = verts.readline()
splitLine = firstline.split('_')
points=[]
points.append([float(splitLine[1]),float(splitLine[2])])
#Creates an array of the Coordinates of the Cities
for line in verts:
    splitLine = line.split('_')
    points.append([float(splitLine[1]), float(splitLine[2])])
    
#Convert the pythonic array into a numpy array
result=np.array(points)

#Run the Delaunay triangulation on the points
tri = Delaunay(result)
plt.triplot(result[:,0], result[:,1], tri.simplices.copy())
plt.plot(result[:,0], result[:,1], 'o')
plt.show()

#Gets the neighboring edges from the Delaunay Triangulation
connections = find_edges(tri)

#Remove duplicate edge connections
for conn in connections:
    for conn2 in connections:
        if conn[0] == conn2[1] and conn[1] == conn2[0]:
            connections.remove(conn2)

adjmat=[]
#Create an NxN matrix of Zeros
for index in range(0,len(points)):
    adjmat.append([0] * 372)

#Fill in the matrix with distances between neighboring verices
for conn in connections:
    #Computes distance based on longitude and latitude
    adjmat[conn[0]][conn[1]] = sqrt((points[conn[0]][0] - points[conn[1]][0])**2\
    + (points[conn[0]][1] - points[conn[1]][1])**2)
    adjmat[conn[1]][conn[0]] = adjmat[conn[0]][conn[1]]

#Runs Prim's algorithm on our adjacency matrix
dij = minimum_spanning_tree(adjmat)
#Converts output to readable array
dijmat = dij.toarray()
edgelist = []
#Finds nonzero values in output adjacency matrix and creates an Edge
for i in range(len(dijmat)):
    for j in range(len(dijmat)):
        if dijmat[i][j] != 0:
            edgelist.append([i , j])
#Converts Pythonic array to Numpy array
edges = np.array(edgelist)
x = result[:,0].flatten()
y = result[:,1].flatten()
plt.figure(figsize=(9,9))
#Plots the graph with only MST Edges shown
plt.plot(x[edges.T], y[edges.T], linestyle='-', color='y',
        markerfacecolor='red', marker='o') 
plt.show()
