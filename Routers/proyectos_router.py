from fastapi import APIRouter, HTTPException
from pymongo import MongoClient


# Enrutador del grupo de endpoints de proyectos
router = APIRouter()


# Cadena de conexion de la base de datos de mongoDB
CONNECTION_STRING = "mongodb://localhost:27017"
client = MongoClient(CONNECTION_STRING) # Conexion al servidor de la base de datos
db = client["Techbridge"]  # Nombre de la base de datos
collection = ""  # Nombre de la colección



# *Endpoint que retorna todos los proyectos
@router.get("/todos-los-proyectos/")
def read_items():
    collection = db["Proyecto"]
    items = list(collection.find())

    return items



# Endpoint que retorna los 5 proyectos mas caros en el año 2024,y que finalizan en 2025 
# ordenados de mayor a menor según su margen de ganancia
@router.get("/proyectos-mas-caros-2024-2025/")
def obtener_proyectos_caros():
    collection = db["Proyecto"]
    try:
        # Ejecutando la consulta
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

        # Convertir los resultados a lista
        resultados_lista = list(resultados)

        # Arrojar una excepcion si no se encontraron resultados
        if not resultados_lista:
            raise HTTPException(status_code=404, detail="No se encontraron proyectos")

        return resultados_lista

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


# Endpoint que devuelve los Proyectos con un margen de ganancia mayor a 10,000 que se encuentran
# en estado Finalizado   
@router.get("/proyectos-finalizados-ganancia-10000/")
def obtener_proyectos_finalizados():
    collection = db["Proyecto"]
    try:
        # Ejecutando la consulta
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

        # Convirtiendo los resultados en una lista
        resultados_lista = list(resultados)

        # Validar la lista, si esta vacia arroja un error
        if not resultados_lista:
            raise HTTPException(status_code=404, detail="No se encontraron proyectos")

        return resultados_lista

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))