from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List, Optional
import model

app = FastAPI()

# Cadena de conexión principal => esta se encuentra en la opcion de menu "cadena de
# conexion" de nuestro servidor de mongo
CONNECTION_STRING = "mongodb://techbridgedb:A1qpL25lVUSfeAauhDxrFG8GbRJFhaDZrAJc0lYTlA5OCnpGrEFVOeXlw1xTQipjbSWSNgcHgrrRACDbgvon2Q==@techbridgedb.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@techbridgedb@"

client = MongoClient(CONNECTION_STRING)
db = client["Techbridge"]  # Nombre de la base de datos
collection = ""  # Nombre de la colección


# Endpoint root de la API
@app.get("/")
def root():
    return {"message": "Bienvenido a la API de mongoDB de TechBridge"}


# Endpoint que retorna todos los hitos de los proyectos
@app.get("/cambios-proyecto/", response_model=List[model.CambiosProyecto])
def read_items():
    collection = db["CambiosProyecto"]
    items = list(collection.find())

    return items



# ! Endpoint que retorna todos los hitos de los proyectos
@app.get("/proyectos/", response_model=List[model.Proyecto])
def read_items():
    collection = db["Proyecto"]
    items = list(collection.find())

    return items



# ! Endpoint que retorna todos los hitos de los proyectos
@app.get("/participacion-empleados/", response_model=List[model.Empleado])
def read_items():
    collection = db["ParticipacionEmpleados"]
    items = list(collection.find())

    return items



# Endpoint que retorna todos los hitos de los proyectos
@app.get("/satisfaccion-cliente/", response_model=List[model.Cliente])
def read_items():
    collection = db["SatisfaccionCliente"]
    items = list(collection.find())

    return items



# Endpoint que retorna todos los hitos de los proyectos
@app.get("/equipos-desarrollo/", response_model=List[model.EquipoDesarrollo])
def read_items():
    collection = db["EficienciaEquiposDesarrollo"]
    items = list(collection.find())

    return items



# Endpoint que retorna todos los hitos de los proyectos
@app.get("/seguimiento-errores/", response_model=List[model.ProyectoErrores])
def read_items():
    collection = db["SeguimientoErrores"]
    items = list(collection.find())

    return items



# Endpoint que retorna todos los hitos de los proyectos
@app.get("/analisis-calidad/", response_model=List[model.ProyectoCalidad])
def read_items():
    collection = db["AnalisisCalidadProyecto"]
    items = list(collection.find())

    return items