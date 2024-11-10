from fastapi import APIRouter, HTTPException
from pymongo import MongoClient


# Enrutador del grupo de endpoints de empleado
router = APIRouter()


# Cadena de conexion de la base de datos de mongoDB
CONNECTION_STRING = "mongodb://localhost:27017"
client = MongoClient(CONNECTION_STRING) # Estableciendo conexion con el servidor
db = client["Techbridge"]  # Nombre de la base de datos
collection = ""  # Nombre de la colección


# *Endpoint que retorna todos los hitos de los proyectos
@router.get("/todos-los-empleados/")#, response_model=List[model.Empleado])
def read_items():
    collection = db["Empleado"]
    items = list(collection.find())

    return items



# Endpoint que retorna los Empleados que han trabajado mas de 100 horas
@router.get("/empleados-mas-de-100-horas-trabajadas/")
def obtener_empleados_mas_de_100_horas():
    collection = db["Empleado"]
    try:
        # Ejecutando la consulta
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

        # Convirtiendo los resultados a una lista
        resultados_lista = list(resultados)

        # Validar si la lista esta vacia
        if not resultados_lista:
            raise HTTPException(status_code=404, detail="No se encontraron empleados")

        return resultados_lista

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# Endpoint que retorna los Empleados con un  salario mayor a 2500 con los proyectos en los que
# ha completado mas de 20 tareas 
@router.get("/empleados-salario-2500/")
def obtener_empleados_salario_tareas():
    collection = db["Empleado"]
    try:
        # Ejecutando la consulta
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

        # Convirtiendo los resultados a una lista
        resultados_lista = list(resultados)

        # Validar si la lista tiene datos
        if not resultados_lista:
            raise HTTPException(status_code=404, detail="No se encontraron empleados")

        return resultados_lista

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
