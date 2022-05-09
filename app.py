# conda install -c conda-forge geopandas GEOS PROJ gdal fiona flask requests waitress
import os
import argparse
import geopandas as gpd
from flask import Flask, request, jsonify, make_response
from waitress import serve
port = 8080
def init():
    app = Flask(__name__)
    @app.route("/data", methods=["GET", "OPTIONS"])
    def getRoutesStations():
        if (request.method == "OPTIONS"):
            return cors_pre()


        routes, stations = get_static_data()
        return cors({
            "rutas": routes,
            "estaciones": stations
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
    

def get_static_data():
    processed_path = "geojson"
    stations_url = "stations.json"
    routes_url = "routes.json"
    shape_estaciones_urls = "./storage/estaciones.shp"
    shape_rutas_url = "./storage/rutas.shp"
    stations_path = "./storage/{}/{}".format(processed_path, stations_url)
    routes_path = "./storage/{}/{}".format(processed_path, routes_url)

    stations = readVectors(shape_estaciones_urls).to_json()
    routes = readVectors(shape_rutas_url)
    routes.groupby(by="route")
    routes = routes.to_json()
    return routes, stations

    if( not ( os.path.exists(stations_path) and os.path.exists(routes_path) ) ):
        print("Building GeoJson Cache files: ")
        stations_data = readVectors(shape_estaciones_urls).to_json()
        routes_data = readVectors(shape_rutas_url)
        routes_data.groupby(by="route")
        routes_data = routes_data.to_json()
        
        stations_file = open(stations_path, "a")
        stations_file.write(stations_data)
        stations_file.close()
        
        routes_file = open(routes_path, "a")
        routes_file.write(routes_data)
        routes_file.close()
    
    routes = ""
    GEOJSON_rutas_urls = "./storage/{}/{}".format(processed_path, routes_url)
    if(os.path.exists(GEOJSON_rutas_urls)):
        g = open(GEOJSON_rutas_urls, "w")
        routes = g.read()
        g.close()
    
    stations = ""
    GEOJSON_estaciones_urls = "./storage/{}/{}".format(processed_path, stations_url)
    if(os.path.exists(GEOJSON_estaciones_urls)):
        g = open(GEOJSON_estaciones_urls, "w")
        stations = g.read()
        g.close()                    

def getLastUnits():
    return []
    return geopandas.GeoSeries([])

def readVectors(infile):
    print(os.path.exists(infile))
    if(os.path.exists(infile)):
        print("Translating geo: "+ infile)
        return gpd.read_file(infile)
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