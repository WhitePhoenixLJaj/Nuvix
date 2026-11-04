from modelos import Producto

CATEGORIAS = [
    "Ropa y Accesorios",
    "Deporte y Entretenimiento",
    "Electronicos",
    "Zapatos y Accesorios",
    "Bolsos",
]

PRODUCTOS = [
    Producto("Camisa casual", 24.99, "Camisa de algodon, talla M", "Ropa y Accesorios", stock=15),
    Producto("Balon de futbol", 19.50, "Balon profesional numero 5", "Deporte y Entretenimiento", stock=20),
    Producto("Audifonos inalambricos", 45.00, "Bluetooth con cancelacion de ruido", "Electronicos", stock=8),
    Producto("Tenis deportivos", 59.90, "Ligeros y comodos para correr", "Zapatos y Accesorios", stock=12),
    Producto("Mochila urbana", 32.00, "Resistente al agua, 20 litros", "Bolsos", stock=10),
    Producto("Gorra negra", 12.75, "Ajustable, unisex", "Ropa y Accesorios", stock=25),
    Producto("Pesas ajustables", 38.00, "Par de mancuernas de 5 kg", "Deporte y Entretenimiento", stock=6),
    Producto("Cargador rapido", 15.99, "USB-C de 30W", "Electronicos", stock=30),
    Producto("Botas de cuero", 74.50, "Cuero genuino, talla 42", "Zapatos y Accesorios", stock=5),
    Producto("Bolso de mano", 41.00, "Elegante, con correa desmontable", "Bolsos", stock=9),
    Producto("Reloj digital", 29.90, "Resistente al agua", "Electronicos", stock=14),
    Producto("Chaqueta ligera", 49.00, "Ideal para clima fresco", "Ropa y Accesorios", stock=7),
]

# ID de cada producto: 1, 2, 3...
for _i, _p in enumerate(PRODUCTOS, start=1):
    _p.codigo = _i


# ---- usuarios registrados (se guardan solo mientras el programa esta abierto) ----
# Las dos listas van en paralelo: la contrasena de USUARIOS[i] esta en CLAVES[i]
USUARIOS = []   # objetos Usuario
CLAVES = []     # contrasenas (texto)
