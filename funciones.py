import os
from PIL import Image, ImageTk, ImageDraw, ImageOps

# Carpeta donde esta este archivo: asi las rutas funcionan sin importar
# desde donde se ejecute el programa.
BASE = os.path.dirname(os.path.abspath(__file__))


def ruta(relativa):
    return os.path.join(BASE, relativa)


def cargar_imagen(ruta_imagen, ancho, alto):
    imagen_pil = Image.open(ruta(ruta_imagen))
    imagen_redimensionar = imagen_pil.resize((ancho, alto))
    return ImageTk.PhotoImage(imagen_redimensionar)


def _redondear(img, radio):
    """Devuelve la imagen con las esquinas redondeadas (transparentes)."""
    escala = 4  # se dibuja la mascara mas grande y se reduce para suavizar el borde
    ancho, alto = img.size
    mascara = Image.new("L", (ancho * escala, alto * escala), 0)
    ImageDraw.Draw(mascara).rounded_rectangle(
        (0, 0, ancho * escala - 1, alto * escala - 1), radio * escala, fill=255)
    mascara = mascara.resize((ancho, alto), Image.LANCZOS)
    img = img.convert("RGBA")
    img.putalpha(mascara)
    return img


def _placeholder(ancho, alto):
    """Imagen gris-lila con figuras, para productos sin foto."""
    img = Image.new("RGBA", (ancho, alto), "#EBE4F0")
    d = ImageDraw.Draw(img)
    color = "#CBC3D3"
    cx, cy = ancho // 2, alto // 2
    d.polygon([(cx, cy - 75), (cx - 32, cy - 22), (cx + 32, cy - 22)], fill=color)
    d.ellipse((cx - 85, cy - 5, cx - 25, cy + 55), fill=color)
    d.rounded_rectangle((cx - 10, cy - 5, cx + 50, cy + 55), 10, fill=color)
    return img


def imagen_producto(ruta_imagen, ancho, alto, radio=24):
    """Foto del producto recortada al tamano pedido y con esquinas redondeadas.
    Si no hay foto (o no existe el archivo) usa el placeholder."""
    if ruta_imagen and os.path.exists(ruta(ruta_imagen)):
        img = ImageOps.fit(Image.open(ruta(ruta_imagen)).convert("RGBA"), (ancho, alto))
    else:
        img = _placeholder(ancho, alto)
    return ImageTk.PhotoImage(_redondear(img, radio))
