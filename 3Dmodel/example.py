import pywavefront
import numpy as np
import os
import pickle

from body_measurements.measurement import Body3D

current_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(current_dir, 'data')

def main():
    person = pywavefront.Wavefront(
        os.path.join(data_dir, 'person.obj'),
        create_materials=True,
        collect_faces=True
    )
    faces1 = np.array(person.mesh_list[0].faces)
    faces = np.load('src/tf_smpl/smpl_faces.npy')
    vertices1 = np.array(person.vertices)
    f = open('verts.pkl', 'rb')
    vertices = pickle.load(f, encoding='Latin1')
    vertices = vertices[0]
    f.close()
    print("vertices=", vertices.shape)
    print("face=", faces.shape)
    print("vertices1=", vertices1.shape)
    print("face1=", faces1.shape)
    

    body = Body3D(vertices, faces)

    body_measurements = body.getMeasurements()

    height = body.height()
    chest = body.chest()
    weight = body.weight()
    waist = body.waist()
    hips = body.hip()
    print(chest)
    print(height)
    print(weight)
    print("waist", waist)
    print("hip", hips)


if __name__ == '__main__':
    main()