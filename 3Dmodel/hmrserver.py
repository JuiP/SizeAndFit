import os
from flask import Flask
from flask import request
from demo import main
import requests

app = Flask(__name__)
app.config["DEBUG"]= True


@app.route('/calculate' , methods=['POST'])
def search():
    ans=1
    measurements = main("data/coco1.png")
    r = requests.get("http://0.0.0.0:5000/measure").content
    # print(r)
    return r;  
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=False)
