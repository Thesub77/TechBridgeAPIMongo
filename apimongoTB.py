from fastapi import FastAPI
from Routers.proyectos_router import router as proyectos_router
from Routers.empleados_router import router as empleados_router


# Construir la aplicacion de FastApi
app = FastAPI()


# Endpoint root de la API
@app.get("/")
def root():
    return {"message": "Bienvenido a la API de mongoDB de TechBridge"}


# Agregar los enrutadores del grupo 'proyecto' a la aplicacion de FastApi
app.include_router(proyectos_router, prefix="/proyectos", tags=["proyectos"])


# Agregar los enrutadores del grupo 'empleado' a la aplicacion de FastApi
app.include_router(empleados_router, prefix="/empleados", tags=["empleados"])
