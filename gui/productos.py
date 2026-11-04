import sys
import unicodedata
import tkinter as tk
from funciones import imagen_producto

COLUMNAS = 4
ANCHO_TARJETA = 305
ALTO_TARJETA = 324
ESPACIO = 29          # espacio entre tarjetas
MARGEN_X = 41         # alineado con el boton "Categorias"
ANCHO_IMAGEN = 285
ALTO_IMAGEN = 216


def _normalizar(texto):
    """Minusculas y sin tildes: 'Camisa' y 'camísa' se consideran iguales."""
    sin_tildes = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in sin_tildes if unicodedata.category(c) != "Mn")


def _coincide(producto, texto):
    """True si el texto aparece en el nombre, la categoria o la descripcion."""
    return texto in _normalizar(f"{producto.nombre} {producto.categoria} {producto.descripcion}")


def _crear_tarjeta(padre, producto, al_hacer_clic):
    # contenedor gris + tarjeta blanca desplazada = sombra simple abajo y a la derecha
    sombra = tk.Frame(padre, bg="#D5D5D5", width=ANCHO_TARJETA, height=ALTO_TARJETA)
    sombra.pack_propagate(False)
    tarjeta = tk.Frame(
        sombra,
        bg="#FFFFFF",
        highlightthickness=1,
        highlightbackground="#DBF9F3")
    tarjeta.pack(fill="both", expand=True, padx=(0, 2), pady=(0, 2))

    foto = imagen_producto(producto.imagen, ANCHO_IMAGEN, ALTO_IMAGEN)
    etiqueta_foto = tk.Label(tarjeta, image=foto, bg="#FFFFFF", bd=0)
    etiqueta_foto.image = foto   # OJO: sin esto Python borra la imagen y se ve vacia
    etiqueta_foto.pack(pady=(10, 8))

    textos = [
        tk.Label(tarjeta, text=producto.nombre, bg="#FFFFFF", anchor="w",
                 font=("ABeeZee", -16, "bold")),
        tk.Label(tarjeta, text=producto.descripcion, bg="#FFFFFF", anchor="w",
                 justify="left", wraplength=ANCHO_IMAGEN, fg="#555555",
                 font=("ABeeZee", -13)),
        tk.Label(tarjeta, text=f"C${producto.precio:,.2f}", bg="#FFFFFF", anchor="w",
                 fg="#075055", font=("ABeeZee", -18, "bold")),
    ]
    for t in textos:
        t.pack(fill="x", padx=14, pady=(0, 3))

    # la tarjeta completa responde al clic y muestra la manito
    for w in (sombra, tarjeta, etiqueta_foto, *textos):
        w.bind("<Button-1>", lambda e, p=producto: al_hacer_clic(p))
        w.config(cursor="hand2")
    return sombra


def crear_galeria(ventana, productos, x, y, al_hacer_clic=print):
    """Zona de productos con scroll (rueda del mouse), debajo del menu.
    Ocupa todo el espacio que queda de la ventana desde (x, y), sea cual sea su tamano.
    Devuelve el lienzo, con dos metodos:
      .refrescar()      vuelve a dibujar las tarjetas (tras publicar, actualizar o eliminar)
      .buscar(texto)    muestra solo los productos que coinciden; texto vacio = todos"""
    lienzo = tk.Canvas(ventana, bd=0, highlightthickness=0, bg="#FFFFFF")
    # relwidth/relheight=1 -> mismo tamano que la ventana; width/height negativos -> menos x e y
    lienzo.place(x=x, y=y, relwidth=1, relheight=1, width=-x, height=-y)

    rejilla = tk.Frame(lienzo, bg="#FFFFFF")
    lienzo.create_window(MARGEN_X, 0, window=rejilla, anchor="nw")

    filtro = {"texto": ""}   

    def dibujar(volver_arriba=False):
        posicion = lienzo.yview()[0]          
        for hijo in rejilla.winfo_children():
            hijo.destroy()

        texto = _normalizar(filtro["texto"].strip())
        lista = [p for p in productos if _coincide(p, texto)] if texto else list(productos)

        if not lista:
            tk.Label(rejilla, bg="#FFFFFF", fg="#555555", font=("ABeeZee", -18),
                     text=f'No se encontraron productos para "{filtro["texto"].strip()}".'
                     ).grid(row=0, column=0, columnspan=COLUMNAS, sticky="w", pady=30)
        for i, producto in enumerate(lista):
            fila, columna = divmod(i, COLUMNAS)
            tarjeta = _crear_tarjeta(rejilla, producto, al_hacer_clic)
            tarjeta.grid(row=fila, column=columna, padx=(0, ESPACIO), pady=(0, ESPACIO - 6))

        # el area desplazable mide lo mismo que el contenido
        rejilla.update_idletasks()
        lienzo.config(
            scrollregion=(0, 0, rejilla.winfo_reqwidth() + MARGEN_X * 2, rejilla.winfo_reqheight() + 10),
            yscrollincrement=20)
        lienzo.yview_moveto(0 if volver_arriba else posicion)

    def buscar(texto):
        filtro["texto"] = texto
        dibujar(volver_arriba=True)

    dibujar()
    # .refrescar() conserva la busqueda activa y vuelve a leer la lista que modifica la ventana de Vender
    lienzo.refrescar = dibujar
    lienzo.buscar = buscar

    def rueda(evento):
        # la rueda solo mueve la galeria si el mouse esta en la ventana principal;
        # en las ventanas emergentes (login, Vender) no debe mover lo que hay detras
        try:
            if evento.widget.winfo_toplevel() is not ventana:
                return
        except (AttributeError, tk.TclError):
            return
        if evento.num == 4:          # Linux: rueda arriba
            pasos = -3
        elif evento.num == 5:        # Linux: rueda abajo
            pasos = 3
        elif sys.platform == "darwin":
            pasos = -evento.delta
        else:                        # Windows
            # el touchpad manda valores pequenos (<120): hay que moverse al menos 1 paso
            pasos = -round(evento.delta / 40) or (-1 if evento.delta > 0 else 1)
        lienzo.yview_scroll(pasos, "units")

    lienzo.bind_all("<MouseWheel>", rueda)
    lienzo.bind_all("<Button-4>", rueda)
    lienzo.bind_all("<Button-5>", rueda)
    return lienzo
