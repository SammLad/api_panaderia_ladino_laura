"""
Módulo de Base de Datos en Memoria (database.py)
Almacena temporalmente los objetos durante la ejecución de Uvicorn.
"""

from typing import List
from models import Pedido
from uuid import uuid4

# Lista global que actúa como muestra de pedidos
db_pedidos: List[Pedido] = []


def cargar_datos_semilla():
    """Carga registros iniciales de prueba (Seed Data) al iniciar la API"""
    if not db_pedidos:
        db_pedidos.extend(
            [
                Pedido(
                    id=uuid4(),
                    producto_reposteria="Torta de Chocolate Fudge",
                    cliente="Laura Garzón",
                    precio_total=85000.0,
                    entregado=True,
                ),
                Pedido(
                    id=uuid4(),
                    producto_reposteria="Cheesecake de Frutos Rojos",
                    cliente="Diana Rodriguez",
                    precio_total=95000.0,
                    entregado=False,
                ),
                Pedido(
                    id=uuid4(),
                    producto_reposteria="Ponqué Tradicional Vino",
                    cliente="Juan Henao",
                    precio_total=120000.0,
                    entregado=True,
                ),
            ]
        )
