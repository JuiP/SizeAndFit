import numpy as np
import trimesh
import math
import matplotlib.pyplot as plt
import geopandas as gpd

def sectionCalc(mesh, levels):
    sections = mesh.section_multiplane(plane_origin=mesh.centroid,plane_normal=[0,1,0],heights=levels)
    
    #remove sections that are NULL
    new_formed_sections = []
    for item in sections:
        if item != None:
            # item.show()
            new_formed_sections.append(item)

    #view the combined sections
    # combined = np.sum(new_formed_sections)
    # combined.show()
    return new_formed_sections

def armpitCalc(sections):
    location = 16 # percentage
    approx_loc = math.floor(location*len(sections)/100)

    #checking 10 sections above and below
    upper_bound = approx_loc + 10
    lower_bound = approx_loc - 10
    # st = sections[lower_bound]
    # combined = np.sum(st)
    # combined.show()

    # st = sections[lower_bound : upper_bound]
    # combined = np.sum(st)
    # combined.show()


    range_sections = range(lower_bound, upper_bound)
    armpits_position = None
    armpits_section = None
    armpits_length = None

    #finding armpits
    for index in range_sections:
        if len(sections[index].entities) == 1:
            armpits_position = index
            armpits_section = sections[index]
            armpits_length = sections[index].polygons_closed[0].length
            # p = gpd.GeoSeries(sections[index].polygons_closed[0])
            # p.plot()
            # plt.show()
            break
                
    return armpits_position

def chestCalc (sections, armpits_location):
    start = armpits_location
    stop = False

    minimum = 100

    chest_position = None
    chest_section = None
    chest_length = None

    while True:
        polygon = largestPolygon(sections[start])
        polygon_min_X = polygon.bounds[0] #min x
        if minimum > polygon_min_X :
            chest_position = start
            chest_section = sections[start]
            chest_length = polygon.length
            minimum = polygon_min_X
            start = start - 1
        else:
            break
        
    return chest_position, chest_length+0.32

def crotchCalc(sections):
    location = 10 # percentage
    approx_loc = math.floor(location*len(sections)/100)

    #range between +-15
    lower_bound = approx_loc - 15
    upper_bound = approx_loc + 15

    range_sections = range(lower_bound, upper_bound)
    
    crotch_position = None
    crotch_section = None
    crotch_length = None

    for index in range_sections:
        if len(sections[index].entities) == 1:
            crotch_position = index
            crotch_section = sections[index]
            crotch_length = sections[index].polygons_closed[0].length
            # p = gpd.GeoSeries(sections[index].polygons_closed[0])
            # p.plot()
            # plt.show()
            break
                
    return crotch_position

def hipCalc(sections, crotch_location):
    start = crotch_location
    maximum = 0

    hip_position = None
    hip_section = None
    hip_length = None

    # find the section till the largest polygon is increasing, increment checked by value of x coordinate
    while True:
        polygon = largestPolygon(sections[start])
        polygon_max_X = polygon.bounds[2] # max X
        if maximum < polygon_max_X :
            hip_position = start
            hip_section = sections[start]
            hip_length = polygon.length
            maximum = polygon_max_X
            start += 1
        else:
            break

    return hip_position, hip_length+0.10

def waistCalc(sections, hip_location):
    start = hip_location
    minimum = 999

    waist_position = None
    waist_section = None
    waist_length = None
    while True:
        polygon = largestPolygon(sections[start])
        polygon_max_X = polygon.bounds[2] #max X
        if minimum > polygon_max_X  :
            waist_position = start
            waist_section = sections[start]
            waist_length = polygon.length
            minimum = polygon_max_X
            start +=  1
        else:
            break
        
    return waist_position, waist_length

def outerLegCalc(sections, hip_location, size_slice):
    approx_loc_ankle = ankleCalc(sections)
    return (hip_location - approx_loc_ankle)*size_slice

def innerLegCalc(sections, crotch_location, size_slice):
    approx_loc_ankle = ankleCalc(sections)
    return ((crotch_location - 1) - approx_loc_ankle)*size_slice

def thighCalc(sections, crotch_location):
    thigh_location = crotch_location - 1
    polygon = largestPolygon(sections[thigh_location])
    return thigh_location, polygon.length

def ankleCalc(sections):
    location_percentage_ankle =  5.65 # percentage
    return math.floor(location_percentage_ankle*len(sections)/100)

def neckCalc(sections):
    location_percentage_neck =  86.25 # percentage
    approx_loc_neck = math.floor(location_percentage_neck*len(sections)/100)
    polygon = largestPolygon(sections[approx_loc_neck])
    return approx_loc_neck, polygon.length

def neckHipCalc(neck_location, hip_location, size_slice):
    return (neck_location - hip_location)*size_slice
                              
def largestPolygon(section):
    #finding ploygon with max area in a given sections
    max_area = 0
    largest_polygon = None
    for polygon in section.polygons_closed:
        if polygon != None:
            if max_area < polygon.area :
                largest_polygon = polygon
                max_area = polygon.area
    return largest_polygon

def heightCalc(mesh):
    slice_r = mesh.section(plane_origin=mesh.centroid, 
                     plane_normal=[0,0,1])
    slice_2D, _ = slice_r.to_planar()
    minY = slice_2D.bounds[0][1]
    maxY = slice_2D.bounds[1][1]
    return (maxY - minY) # meters

def weightCalc(mesh):
    body_density = 0.985
    return (mesh.volume*1000) * body_density

class Body3D(object):
    def __init__(self, vertices, faces, steps=0.005, levels=[-1.5, 1.5]):
        self.vertices = vertices
        self.faces = faces
        self.steps = steps
        self.levels = np.arange(levels[0], levels[1], step=self.steps)
        
        #initializing a mesh
        self.mesh = trimesh.Trimesh(self.vertices, self.faces)

        #visualize mesh
        # self.mesh.show()

        #generate sections that are not NULL
        self.sections = sectionCalc(self.mesh, self.levels)

        # approx locations of armpits crotch and hip 
        self.armpits_location = armpitCalc(self.sections)
        self.crotch_location = crotchCalc(self.sections)
        self.hip_location, _ = hipCalc(self.sections, self.crotch_location)

    def getMeasurements(self):
        #all measurements
        weight = weightCalc(self.mesh)
        height = heightCalc(self.mesh)
        chest_location, chest_length = chestCalc(self.sections, self.armpits_location)
        hip_location, hip_length = hipCalc(self.sections, self.crotch_location)
        waist_location, waist_length = waistCalc(self.sections, self.hip_location)
        thigh_location, thigh_length = thighCalc(self.sections, self.crotch_location)
        outer_leg_length = outerLegCalc(self.sections, self.hip_location, self.steps)
        inner_leg_length = innerLegCalc(self.sections, self.crotch_location, self.steps)
        neck_location, neck_length = neckCalc(self.sections)
        neck_hip_length = neckHipCalc(neck_location, self.hip_location, self.steps)

        return weight, height, chest_length, hip_length, waist_length, thigh_length, outer_leg_length, inner_leg_length, neck_hip_length

