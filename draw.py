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

# inputs
i=0
wire_radius = 0.16
insulation_thickness = 1.6


filename = '1064.txt'
filename2 = 'radii.txt'
with open(filename) as f:
    cable_data = f.read()
cable_data = cable_data.split('\n')
with open(filename2) as f2:
    radii = f2.read()
radii = radii.split(',')
#print(cable_data)
i=0	
#def draw_cables():
a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['cable_1']
no_of_cables = int(filename.replace('.txt',""))
ratio = (float(radii[no_of_cables]) / wire_radius)
#print("ratio",ratio)

outer_radius = round((1 / ratio), 5)
for instancja in cable_data:
    #print('a')
    #print(instancja.split(',')[0])
    #print(instancja.split(',')[1])
    a.Instance(name='cable_1-'+str(i), part=p, dependent=ON)
    a.translate(instanceList=('cable_1-'+str(i), ), vector=(0.0,float(instancja.split(',')[0])/ratio, float(instancja.split(',')[1])/ratio))
    i=i+1

# draw insulation

s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
        sheetSize=200.0)
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
s1.setPrimaryObject(option=STANDALONE)
s1.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(3.75, 3.75))
s1.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(7.5, 7.5))
s1.RadialDimension(curve=g[3], textPoint=(-14.1078071594238, 14.2295074462891), 
	radius=outer_radius+insulation_thickness)
s1.RadialDimension(curve=g[2], textPoint=(17.0899429321289, 15.4918022155762), 
	radius=outer_radius)
p = mdb.models['Model-1'].Part(name='insulation', dimensionality=THREE_D, 
	type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['insulation']
p.BaseSolidExtrude(sketch=s1, depth=150.0)
s1.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['insulation']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']
a1 = mdb.models['Model-1'].rootAssembly
a1.regenerate()
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
a1 = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['insulation']
a1.Instance(name='insulation-2', part=p, dependent=ON)
a1 = mdb.models['Model-1'].rootAssembly
a1.rotate(instanceList=('insulation-2', ), axisPoint=(0.0, 0.0, 0.0), 
	axisDirection=(0.0, 1.0, 0.0), angle=90.0)
a.translate(instanceList=('insulation-2', ), vector=(-75.0,0,0))
