import pywavefront
import numpy as np
import os
import pickle

from body_measurements.measurement import Body3D

current_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(current_dir, 'data')

def main():
    faces = np.load('src/tf_smpl/smpl_faces.npy')

    f = open('verts.pkl', 'rb')
    vertices = pickle.load(f, encoding='Latin1')
    vertices = vertices[0]
    f.close()
    
    body = Body3D(vertices, faces)

    body_measurements = body.getMeasurements()
    print("body measurements")

    print("weight",body_measurements[0])
    print("height",body_measurements[1]*100 ,"cms")
    print("chest length",body_measurements[2])
    print("hip length",body_measurements[3])
    print("waist length",body_measurements[4])
    print("thigh length", body_measurements[5]) 
    # print("outer leg length", body_measurements[6])
    # print("inner leg length",body_measurements[7])
    # print("neck hip length",body_measurements[8])
    


if __name__ == '__main__':
    main()