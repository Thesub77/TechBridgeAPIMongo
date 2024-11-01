from pydantic import BaseModel
from typing import List, Optional


# Clase modelo de los Item
class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = False


## * Modelos de la coleccion "CambiosProyecto"

# Clase modelo de la coleccion embebida que representa el "Historial de cambios de los proyectos"
class HistorialCambios(BaseModel):
    fecha: str
    cambio: str
    detalles: str
    estado: str


# Clase modelo de la coleccion que representa los "Cambios del proyecto"
class CambiosProyecto(BaseModel):
    _id: str
    project_id: str
    historial_cambios: List[HistorialCambios]
    ultimo_cambio_implementado: str

    class Config:
        arbitrary_types_allowed = True


## * Modelos de la coleccion "Proyecto"

# Clase modelo de la coleccion embebida que representa los "Requerimientos del proyecto"
class Requerimiento(BaseModel):
    tipo_requerimiento: str
    descripcion: str


# Clase modelo de la coleccion embebida que representa los "Pagos realizados a los proyectos"
class Pago(BaseModel):
    fecha: str
    monto: float
    comentario: str


# Clase modelo de la coleccion embebida que representa el "Seguimiento de avances del proyecto"
class SeguimientoProyecto(BaseModel):
    fecha: str
    nota: str
    responsable: str


# Clase modelo de la coleccion que representa los "Proyectos de software"
class Proyecto(BaseModel):
    _id: str
    project_id: str
    cliente_id: str
    equipo_id: str
    nombre_proyecto: str
    descripcion_proyecto: str
    fecha_inicio: str
    fecha_fin: Optional[str] = None
    margen_ganancia: float
    requerimientos: List[Requerimiento]
    pagos: List[Pago]
    seguimientoProyecto: List[SeguimientoProyecto]
    herramientas_utilizadas: List[str]
    metodologias_utilizadas: List[str]
    estado: str
    fecha_entrega: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True


## * Modelos de la coleccion "ParticipacionEmpleado"

# Clase modelo de la coleccion embebida que representa la "Participacion de empleados en proyectos"
class ParticipacionProyecto(BaseModel):
    project_id: str
    rol: str
    horas: int
    tareas_completadas: int
    comentarios: str


# Clase modelo de la coleccion que representa los "Empleados de la empresa desarrolladora"
class Empleado(BaseModel):
    _id: str
    employee_id: str
    nombres: str
    apellidos: str
    cargo: str
    fecha_contratado: str
    salario: float
    participacion_proyectos: List[ParticipacionProyecto]

    class Config:
        arbitrary_types_allowed = True


## * Modelos de la coleccion "SatisfaccionCliente"

# Clase modelo de la coleccion embebida que representa la "Retroalimentacion de los clientes
# hacia los proyectos"
class SeguimientoSatisfaccion(BaseModel):
    proyecto_id: str
    fecha: str
    comentario: str
    satisfaccion: str
    sugerencias: str


# Clase modelo de la coleccion que representa los "Clientes de la desarrolladora"
class Cliente(BaseModel):
    _id: str
    cliente_id: str
    nombre_compania: str
    contacto: str
    direccion: str
    seguimientoSatisfaccion: List[SeguimientoSatisfaccion]

    class Config:
        arbitrary_types_allowed = True


## * Modelos de la coleccion "EficienciaEquiposDesarrollo"

# Clase modelo de la coleccion embebida que representa el "Rendimiento de los equipos de trabajo"
class Rendimiento(BaseModel):
    proyecto_id: str
    fecha: str
    horas_trabajadas: int
    tareas_completadas: int


# Clase modelo de la coleccion que representa los "Equipos de desarrollo"
class EquipoDesarrollo(BaseModel):
    _id: str
    equipo_id: str
    id_empleados_miembros_equipo: List[str]
    rendimiento: List[Rendimiento]
    rendimiento_general: str

    class Config:
        arbitrary_types_allowed = True


## * Modelos de la coleccion "SeguimientoErrores"

# Clase modelo de la coleccion embebida que representa los "Detalles de los errores y sus soluciones"
class Error(BaseModel):
    error_id: str
    descripcion: str
    gravedad: str
    fecha: str
    estado: str
    solucion: Optional[str] = None


# Clase modelo de la coleccion que representa los "Errores detectados en los proyectos"
class ProyectoErrores(BaseModel):
    _id: str
    proyecto_id: str
    errores: List[Error]
    ultimo_error_detectado: str
    ultimo_error_resuelto: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True


## * Modelos de la coleccion "AnalisisCalidadProyecto"

# Clase modelo de la coleccion embebida que representa los 
# "Detalles de todos los analisis de calidad realizados en el proyecto"
class AnalisisCalidad(BaseModel):
    fecha_analisis: str
    etapa_proyecto: str
    nota: str
    calificacion: float
    responsable: str


# Clase modelo de la coleccion que representa los "Analisis de calidad en diferentes fases del proyecto"
class ProyectoCalidad(BaseModel):
    _id: str
    project_id: str
    analisisCalidad: List[AnalisisCalidad]
    ultimo_analisis: str

    class Config:
        arbitrary_types_allowed = True