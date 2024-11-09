from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List, Optional
import model

app = FastAPI()

# Cadena de conexión principal => esta se encuentra en la opcion de menu "cadena de
# conexion" de nuestro servidor de mongo
# CONNECTION_STRING = "mongodb://techbridgedb:A1qpL25lVUSfeAauhDxrFG8GbRJFhaDZrAJc0lYTlA5OCnpGrEFVOeXlw1xTQipjbSWSNgcHgrrRACDbgvon2Q==@techbridgedb.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@techbridgedb@"
CONNECTION_STRING = "mongodb://localhost:27017"
client = MongoClient(CONNECTION_STRING)
db = client["Techbridge"]  # Nombre de la base de datos
collection = ""  # Nombre de la colección


# Endpoint root de la API
@app.get("/")
def root():
    return {"message": "Bienvenido a la API de mongoDB de TechBridge"}



# Endpoint que retorna todos los hitos de los proyectos
@app.get("/proyectos/")#, response_model=List[model.Proyecto])
def read_items():
    collection = db["Proyecto"]
    items = list(collection.find())

    return items



@app.get("/proyectos-caros/")#, response_model=List[model.Proyecto])
def obtener_proyectos_caros():
    collection = db["Proyecto"]
    try:
        # Consulta directa con filtros y ordenación
        resultados = (
            collection.find(
                {"fecha_inicio": {"$regex": "^2024"}, "fecha_fin": {"$regex": "^2025"}},
                {
                    "_id": 0,
                    "proyecto_id": 1,
                    "nombre_proyecto": 1,
                    "margen_ganancia": 1,
                    "fecha_inicio": 1,
                    "fecha_fin": 1,
                },
            )
            .sort("margen_ganancia", -1)  # Ordenar de mayor a menor
            .limit(5)  # Limitar a 5 resultados
        )

        resultados_lista = list(resultados)

        if not resultados_lista:
            raise HTTPException(status_code=404, detail="No se encontraron proyectos")

        return resultados_lista

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/proyectos-finalizados/")
def obtener_proyectos_finalizados():
    collection = db["Proyecto"]
    try:
        # Consulta directa con filtros y agregación
        resultados = (
            collection.aggregate([
                {
                    "$match": {
                        "margen_ganancia": {"$gt": 10000},
                        "estado": "Finalizado"
                    }
                },
                {
                    "$sort": {"fecha_inicio": 1}
                },
                {
                    "$limit": 10
                },
                {
                    "$project": {
                        "_id": 0,
                        "proyecto_id": 1,
                        "nombre_proyecto": 1,
                        "margen_ganancia": 1,
                        "fecha_inicio": 1,
                        "estado": 1
                    }
                }
            ])
        )

        resultados_lista = list(resultados)

        if not resultados_lista:
            raise HTTPException(status_code=404, detail="No se encontraron proyectos")

        return resultados_lista

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# Endpoint que retorna todos los hitos de los proyectos
@app.get("/empleados/")#, response_model=List[model.Empleado])
def read_items():
    collection = db["Empleado"]
    items = list(collection.find())

    return items



@app.get("/empleados-mas-de-100-horas/")
def obtener_empleados_mas_de_100_horas():
    collection = db["Empleado"]
    try:
        # Consulta de agregación para obtener empleados con más de 100 horas
        resultados = (
            collection.aggregate([
                {
                    "$project": {
                        "_id": 0,
                        "employee_id": 1,
                        "nombres": 1,
                        "apellidos": 1,
                        "total_horas": {"$sum": "$participacion_proyectos.horas"}
                    }
                },
                {
                    "$match": {
                        "total_horas": {"$gt": 100}
                    }
                }
            ])
        )

        resultados_lista = list(resultados)

        if not resultados_lista:
            raise HTTPException(status_code=404, detail="No se encontraron empleados")

        return resultados_lista

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/empleados-salario-tareas/")
def obtener_empleados_salario_tareas():
    collection = db["Empleado"]
    try:
        # Consulta de agregación para obtener empleados con salario > 2500 y más de 20 tareas completadas
        resultados = (
            collection.aggregate([
                {
                    "$match": {
                        "salario": {"$gt": 2500},
                        "participacion_proyectos.tareas_completadas": {"$gt": 20}
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "employee_id": 1,
                        "nombres": 1,
                        "apellidos": 1,
                        "salario": 1,
                        "participacion_proyectos": {
                            "$filter": {
                                "input": "$participacion_proyectos",
                                "as": "proyecto",
                                "cond": {"$gt": ["$$proyecto.tareas_completadas", 20]}
                            }
                        }
                    }
                }
            ])
        )

        resultados_lista = list(resultados)

        if not resultados_lista:
            raise HTTPException(status_code=404, detail="No se encontraron empleados")

        return resultados_lista

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
