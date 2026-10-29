"""
Módulo Principal de la Aplicación (main.py)
Instancia FastAPI, expone los endpoints, RESTful y gestiona excepciones
"""

from fastapi import FastAPI, HTTPException, status
from typing import List
from uuid import UUID

from models import Pedido, PedidoCreate, PedidoUpdate
from database import db_pedidos, cargar_datos_semilla

# Instancia de FastAPI con metadata profesional
app = FastAPI(
    title="API Panadería / Pastelería - SENA ADSO",
    description="API RESTful para la gestión pedidos de repostería en memoria utilizando Pydantic y FastAPI.",
    version="1.0.0",
)


# cargar datos iniciales al arrancar la aplicación
@app.on_event("startup")
def startup_event():
    cargar_datos_semilla()


# ===================================================
# ENDPOINTS Y LÓGICA DEL CRUD
# ===================================================


@app.get("/", tags=["Raiz"], summary="Mensaje da Bienvenida")
def welcome():
    return {
        "mensaje": "Bienvenido a la API de Pedidos de Repostería (SENA ADSO)",
        "documentacion": "/docs",
    }


@app.get(
    "/pedidos",
    response_model=List[Pedido],
    status_code=status.HTTP_200_OK,
    tags=["Pedidos"],
    summary="Obtener todo los pedidos",
)
def get_pedidos():
    """Devuelve la lista completa de pedidos registrados en memoria."""
    return db_pedidos


@app.get(
    "/pedidos/{pedido_id}",
    response_model=Pedido,
    status_code=status.HTTP_200_OK,
    tags=["Pedidos"],
    summary="Buscar pedidos por ID",
)
def get_pedido_por_id(pedido_id: UUID):
    """
    Busca un pedido específico mediante su identificador UUID.
    - Lanza HTTP 404 Not Found si el pedido no existe en memoria.
    """
    for pedd in db_pedidos:
        if pedd.id == pedido_id:
            return pedd

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"El pedido con ID '{pedido_id}' no fue encontrado en los registros.",
    )


@app.post(
    "/pedidos",
    response_model=Pedido,
    status_code=status.HTTP_201_CREATED,
    tags=["Pedidos"],
    summary="Agregar nuevo pedido",
)
def create_pedido(pedido_in: PedidoCreate):
    """
    - Valida automáticamente que el `precio` sea mayor a 0 (gt=0).
    - Asigna un `id` UUIDv4 único de forma automática.
    - Lanza **HTTP 400 Bad Request** si el cliente ya se encuentra registrado.
    """

    # Validación personalizada: Evitar duplicados por cliente
    for pedd in db_pedidos:
        if pedd.cliente.lower() == pedido_in.cliente.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un pedido registrado con el cliente '{pedido_in.cliente}'.",
            )

    # Transformar el esquema de entrada al modelo completo con UUID
    nuevo_pedido = Pedido(**pedido_in.model_dump())
    db_pedidos.append(nuevo_pedido)
    return nuevo_pedido


@app.put(
    "/pedidos/{pedido_id}",
    response_model=Pedido,
    status_code=status.HTTP_200_OK,
    tags=["Pedidos"],
    summary="Actualizar pedido por ID",
)
def update_pedido(pedido_id: UUID, pedido_update: PedidoUpdate):
    """
    Actualiza los datos de un pedido existente por su ID UUID:
    - Reemplaza los campos proporcionados de forma segura.
    - Lanza **HTTP 404 Not Found** si el ID solicitado no existe.
    """
    for index, pedd in enumerate(db_pedidos):
        if pedd.id == pedido_id:
            # Extraer solo los campos que fueron enviados en la petición
            datos_actualizados = pedido_update.model_dump(exclude_unset=True)

            # Crear una copia actualizada del objeto mantenimiento su ID original
            pedido_modificado = pedd.model_copy(update=datos_actualizados)
            db_pedidos[index] = pedido_modificado
            return pedido_modificado

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No es posible actualizar. El pedido con ID '{pedido_id}' no existe.",
    )


@app.delete(
    "/pedidos/{pedido_id}",
    status_code=status.HTTP_200_OK,
    tags=["Pedidos"],
    summary="Eliminar pedido por ID",
)
def delete_pedido(pedido_id: UUID):
    """
    - Lanza **HTTP 404 Not Found** si el registro no existe
    """
    for index, pedd in enumerate(db_pedidos):
        if pedd.id == pedido_id:
            pedido_eliminado = db_pedidos.pop(index)
            return {
                "mensaje": "Pedido eliminado exitosamente",
                "pedido_eliminado": pedido_eliminado,
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No es posible eliminar. El pedido con ID '{pedido_id}' no existe.",
    )
