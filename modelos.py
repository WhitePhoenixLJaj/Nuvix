from dataclasses import dataclass

@dataclass
class Usuario:
    nombre: str
    apellido: str
    nombre_usuario: str
    correo_electronico: str
    telefono: str


@dataclass
class Producto:
    nombre: str
    precio: float
    descripcion: str
    categoria: str
    imagen: str = ""   # ruta de la foto; si queda vacia se muestra el placeholder
    stock: int = 0     # unidades disponibles (se administra en la ventana de Vender)
    codigo: int = 0    # ID del producto (se asigna en datos.py o al publicar uno nuevo)
