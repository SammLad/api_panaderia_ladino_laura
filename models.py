"""
Módulo de Modelos de Datos
Define la estructura, tipo de datos y validadciones con Pydantic
"""

"""
producto_reposteria, 
cliente, precio_total, 
entregado 
"""

from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID, uuid4


class PedidoBase(BaseModel):
    producto_reposteria: str = Field(
        ...,
        min_length=2,
        max_length=100,
        descripcion="Nombre del producto de repostería",
        example="Mantecada",
    )
    cliente: str = Field(
        ...,
        min_length=2,
        max_length=100,
        descripcion="Nombre del producto de repostería",
        example="Laura Garzón",
    )
    precio_total: float = Field(
        ...,
        gt=0,
        description="Precio unitario en COP/USD. Debe ser estrictamente mayor a 0.",
        example=4500.00,
    )
    entregado: bool = Field(
        default=True, description="Estado de disponibilidad en el inventario"
    )


class PedidoCreate(PedidoBase):
    """Modelo utilizado para recibir solicitudes en el inventario"""

    pass


class PedidoUpdate(BaseModel):
    """Modelo para solicitudes PUT (Campos opcionales para edición)"""

    producto_reposteria: Optional[str] = Field(None, min_length=2, max_length=100)
    cliente: Optional[str] = Field(None, min_length=2, max_length=100)
    precio_total: Optional[float] = Field(None, gt=0)
    entregado: Optional[bool] = Field(None)


class Pedido(PedidoBase):
    """Modelo completo de respuesta que incluye el ID autogenerado"""

    id: UUID = Field(
        default_factory=uuid4, description="Identificador Único Universal (UUIDv4)"
    )

    class Config:
        from_attributes = True
