# conda install -c conda-forge geopandas GEOS PROJ gdal fiona flask requests waitress
import os
import argparse
import geopandas as gpd
from flask import Flask, request, jsonify, make_response
from waitress import serve
port = 8080
def init():
    app = Flask(__name__)
    @app.route("/data/static", methods=["GET", "OPTIONS"])
    def get_static_data():
        if (request.method == "OPTIONS"):
            return cors_pre()
        args = (request.args).to_dict()
        scoped = "full service"
        if(args.__contains__("route")):
            scoped = args.route
        print("Fetching static shape files for: "+scoped)
        estaciones_url = "./storage/estaciones.shp"
        rutas_url = "./storage/rutas.shp"
        estaciones_data = readVectors(estaciones_url)
        rutas_data = readVectors(rutas_url)
        
        return cors({
            "rutas": rutas_data,
            "estaciones": estaciones_data
        })
    
    @app.route("/data/db", methods=["GET", "OPTIONS"])
    def get_db_data():
        if (request.method == "OPTIONS"):
            return cors_pre()
        #requests(endpoint)
        units = getLastUnits()
        return cors({
            "unidades": units
        })

    #app.run(ssl_context=('cert.pem', 'key.pem'))
    print("Initialized app on port {}".format(port))
    serve(app, listen='*:'+str(port))

def getLastUnits():
    return []

def readVectors(infile):
    print(os.path.exists(infile))
    if(os.path.exists(infile)):
        print("Translating geo: "+ infile)
        data = gpd.read_file(infile)
        return data.to_json()
    else:
        print("file not found: "+ infile)


def cors_pre():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def cors(body):
    response = make_response(body)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == "__main__":
    init()