import os
from flask import Flask
from flask import request
from body_measurements.measurement import Body3D
import numpy as np
import os
import pickle

app = Flask(__name__)
app.config["DEBUG"]= True


@app.route('/measure' , methods=['GET'])
def search():
    faces = np.load('src/tf_smpl/smpl_faces.npy')

    f = open('verts.pkl', 'rb')
    vertices = pickle.load(f, encoding='Latin1')
    vertices = vertices[0]
    f.close()
    
    body = Body3D(vertices, faces)

    body_measurements = body.getMeasurements()
    measure_dict ={}
    measure_dict["weight"] = body_measurements[0]
    measure_dict["height"] = body_measurements[1]*100
    measure_dict["chest length"] = body_measurements[2]
    measure_dict["hip length"] = body_measurements[3]
    measure_dict["waist length"] = body_measurements[4]
    measure_dict["thigh length"] = body_measurements[5]

    print("body measurements")
    print("weight",body_measurements[0])
    print("height",body_measurements[1]*100 ,"cms")
    print("chest length",body_measurements[2])
    print("hip length",body_measurements[3])
    print("waist length",body_measurements[4])
    print("thigh length", body_measurements[5])
    return measure_dict;  
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
