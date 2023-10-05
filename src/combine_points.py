# Disch data will contain: the 3 coords of the first point in each beam, the
# beamlength, rotational degree and normalvector for rotation.
import csv
import numpy as np
def read_matrix(filename, num_type=float): #function for reading a data file
    return np.genfromtxt(filename,delimiter=',', dtype=num_type)

def data_gathering():
    coord = read_matrix('/Users/simeon/Desktop/ETH/Semester Project/GenerateTruss/Coord.dat')
    C = read_matrix('/Users/simeon/Desktop/ETH/Semester Project/GenerateTruss/C.dat', num_type=int)
    data=np.zeros([len(C),7])
    temp=np.zeros([len(C),3])
    print("Shape of coord:", coord.shape)
    print("Shape of C:", C.shape)
    print("Values of C[:,0]:", C[:,0])

    data[:,:3] = coord[C[:,0],:3] #coords of start point
    temp[:,:3] = coord[C[:,1],:3] #coords of end point

    data[:,6] = temp[:,0] - data[:,0] #y-direction of normal vector
    data[:,5] = data[:,1] - temp[:,1] #x-direction of normal vector
    data[:,3] = ((data[:,0] - temp[:,0])**2 + data[:,5]**2 + (data[:,2] - \
        temp[:,2])**2)**0.5 #length of beam
    data[:,4] = 180/np.pi * (np.pi / 2 - np.arcsin((temp[:,2]- data[:,2])/ data[:,3])) #angle to z-axis of beam
    return data

data=data_gathering()
#specify directory 
with open('/Users/simeon/Desktop/ETH/Semester Project/GenerateTruss/Lattice.csv','w',newline='') as f:
    writer = csv.writer(f)
    writer.writerows(data)
