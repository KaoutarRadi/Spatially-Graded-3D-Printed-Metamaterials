# Do not delete the following import lines make sure that there aren't
# any already existing parts or instances in your abaqus workspace
import numpy as np
from abaqus import *
from abaqusConstants import *
import __main__

import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import step
import interaction
import load
import mesh
import optimization
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior
import sys
import stlExport_kernel
#might need adjustment depending on the computer it is used on. 
sys.path.insert(8, 
     r'C:/APPS/SIMULIA/EstProducts/2021/win_b64/code/python2.7/lib/abaqus_plugins/stlExport') #data computer
#One can also export manually by clicking on Plug-ins in the menu-bar, selecting tools->stl export

matrix=np.genfromtxt('G:\\Carbon_3D\\Lattice.csv',delimiter=',',dtype=float) 
#the full structure, adjust according to computer capabilities. must be < n !!
stepsize=500
n=len(matrix)
#n=5
n1=int(n/stepsize)
#apply the sphere at all nodes.
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.ArcByCenterEnds(center=(0.0, 0.0), point1=(0.0, -.5), point2=(0.0,.5), 
    direction=COUNTERCLOCKWISE)
s.Line(point1=(0.0, .5), point2=(0.0, -.5))
s.ConstructionLine(point1=(0.0, -8.75), point2=(0.0, 10.0))
p = mdb.models['Model-1'].Part(name='mergeball', dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['mergeball']
p.BaseSolidRevolve(sketch=s, angle=360.0, flipRevolveDirection=OFF)
s.unsetPrimaryObject()

del mdb.models['Model-1'].sketches['__profile__']
    
for j in range(n1):
    for i in range(j*stepsize,j*stepsize+stepsize):
        s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
        g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
        s1.setPrimaryObject(option=STANDALONE)
        s1.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(0.5, 0.0)) #enter here the desired beam-radius in mm
        p = mdb.models['Model-1'].Part(name='Part-{}'.format(i), dimensionality=THREE_D, 
            type=DEFORMABLE_BODY)
        p = mdb.models['Model-1'].parts['Part-{}'.format(i)]
        p.BaseSolidExtrude(sketch=s1, depth=matrix[i][3]) #here we enter the beam length
        s1.unsetPrimaryObject()
        p = mdb.models['Model-1'].parts['Part-{}'.format(i)]
        del mdb.models['Model-1'].sketches['__profile__']
        a = mdb.models['Model-1'].rootAssembly
        p = mdb.models['Model-1'].parts['Part-{}'.format(i)]
        a.Instance(name='Part-{}-1'.format(i*2), part=p, dependent=OFF)
        p = mdb.models['Model-1'].parts['mergeball']
        a.Instance(name='Part-{}-1'.format(i*2+1),part=p,dependent=OFF)
        a.translate(instanceList=('Part-{}-1'.format(2*i+1),), vector=(matrix[i][0],matrix[i][1],matrix[i][2])) #here, we input the coordinate of the point around which the beam was rotated
        a.rotate(instanceList=('Part-{}-1'.format(2*i),), axisPoint=(0.0, 0.0, 0.0), axisDirection=(matrix[i][5],matrix[i][6], 0.0), angle=matrix[i][4]) #here, we input the normal vector to the rotation first and then the rotation angle
        a.translate(instanceList=('Part-{}-1'.format(2*i),), vector=(matrix[i][0],matrix[i][1],matrix[i][2])) #here, we input the coordinate of the point around which the beam was rotated
    instances = [a.instances['Part-{}-1'.format(i)] for i in range(2*j*stepsize,(j*stepsize+stepsize)*2)] #we merge the just created number of parts into a subpart to be merged again later
    a1 = mdb.models['Model-1'].rootAssembly
    a1.InstanceFromBooleanMerge(name='merge-{}'.format(j), instances=instances, originalInstances=DELETE, domain=GEOMETRY)
    for i in range(j*stepsize,j*stepsize+stepsize):
        del mdb.models['Model-1'].parts['Part-{}'.format(i)] 


for i in range(n1*stepsize,n):
    s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.setPrimaryObject(option=STANDALONE)
    s1.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(0.5, 0.0)) #enter here the desired beam-radius (should be the same as above)
    p = mdb.models['Model-1'].Part(name='Part-{}'.format(i), dimensionality=THREE_D, 
        type=DEFORMABLE_BODY)
    p = mdb.models['Model-1'].parts['Part-{}'.format(i)]
    p.BaseSolidExtrude(sketch=s1, depth=matrix[i][3])
    s1.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts['Part-{}'.format(i)]
    del mdb.models['Model-1'].sketches['__profile__']
    a = mdb.models['Model-1'].rootAssembly
    p = mdb.models['Model-1'].parts['Part-{}'.format(i)]
    a.Instance(name='Part-{}-1'.format(i*2), part=p, dependent=OFF)
    p = mdb.models['Model-1'].parts['mergeball']
    a.Instance(name='Part-{}-1'.format(i*2+1),part=p,dependent=OFF)
    a.translate(instanceList=('Part-{}-1'.format(2*i+1),), vector=(matrix[i][0],matrix[i][1],matrix[i][2])) #here, we input the coordinate of the point around which the beam was rotated
    a.rotate(instanceList=('Part-{}-1'.format(2*i),), axisPoint=(0.0, 0.0, 0.0), axisDirection=(matrix[i][5],matrix[i][6], 0.0), angle=matrix[i][4]) #here, we input the normal vector to the rotation first and then the rotation angle
    a.translate(instanceList=('Part-{}-1'.format(2*i),), vector=(matrix[i][0],matrix[i][1],matrix[i][2])) #here, we input the coordinate of the point around which the beam was rotated

instances = [a.instances['Part-{}-1'.format(i)] for i in range(2*n1*stepsize,2*n)] #we merge the just created number of parts into a subpart to be merged again later
a1 = mdb.models['Model-1'].rootAssembly
a1.InstanceFromBooleanMerge(name='merge-{}'.format(n1), instances=instances, originalInstances=DELETE, domain=GEOMETRY)
    
for i in range(n1*stepsize,n):
        del mdb.models['Model-1'].parts['Part-{}'.format(i)]


for i in range(n1+1): 
    a = mdb.models['Model-1'].rootAssembly
    p = mdb.models['Model-1'].parts['merge-{}'.format(i)]

instances = [a.instances['merge-{}-1'.format(i)] for i in range(n1+1)]
a1 = mdb.models['Model-1'].rootAssembly

a1.InstanceFromBooleanMerge(name='merge-final', instances=instances, originalInstances=DELETE, domain=GEOMETRY) 

#delete the remaining subparts, such that only the final structure remains.
for i in range(n1+1):
    del mdb.models['Model-1'].parts['merge-{}'.format(i)] 

# to export our structure to an .stl file, wedisplay the merged final part as the current one
p1 = mdb.models['Model-1'].parts['merge-final']
session.viewports['Viewport: 1'].setValues(displayedObject=p1)

#write in the directory and filename for the resulting .stl file. one
#can choose 'BINARY' instead of 'ASCII' if so desired
stlExport_kernel.STLExport(moduleName='Part', 
   stlFileName='G:\\Carbon_3D\\Lattice.stl', stlFileType='ASCII') 