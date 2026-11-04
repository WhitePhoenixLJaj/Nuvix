import tkinter as tk
from tkinter import messagebox
from modelos import Producto

_ventana_abierta = None   # solo una ventana de administracion a la vez


def abrir_gestion(principal, productos, al_cambiar=lambda: None):
    """Ventana para publicar, actualizar, eliminar y buscar productos.
    Trabaja sobre la misma lista `productos` que muestra la galeria;
    al_cambiar() se llama despues de cada cambio para que la galeria se redibuje."""
    global _ventana_abierta
    if _ventana_abierta is not None and _ventana_abierta.winfo_exists():
        _ventana_abierta.lift()
        _ventana_abierta.focus_force()
        return

    # Productos que se estan mostrando ahora en la lista (todos o filtrados por busqueda)
    visibles = []

    ventana = tk.Toplevel(principal)
    _ventana_abierta = ventana
    ventana.title("Nuvix - Gestión de Productos")
    ventana.resizable(False, False)
    ventana.transient(principal)
    alto = min(740, ventana.winfo_screenheight() - 90)
    x = principal.winfo_x() + (principal.winfo_width() - 500) // 2
    y = principal.winfo_y() + 20
    ventana.geometry(f"500x{alto}+{max(x, 0)}+{max(y, 0)}")

    # --- FUNCIONES CRUD ---
    def siguiente_codigo():
        return max((p.codigo for p in productos), default=0) + 1

    def crear_producto():
        nombre = entry_nombre.get().strip()
        precio = entry_precio.get().strip()
        categoria = entry_categoria.get().strip()
        stock = entry_stock.get().strip()
        descripcion = entry_descripcion.get().strip()

        if not nombre or not precio or not categoria or not stock or not descripcion:
            messagebox.showwarning("Aviso", "Todos los campos son obligatorios.", parent=ventana)
            return

        try:
            if float(precio) < 0:
                messagebox.showerror("Error", "El precio no puede ser negativo.", parent=ventana)
                return
            if int(stock) < 0:
                messagebox.showerror("Error", "El stock no puede ser negativo.", parent=ventana)
                return
            nuevo = Producto(
                nombre=nombre,
                precio=float(precio),
                descripcion=descripcion,
                categoria=categoria,
                stock=int(stock),
                codigo=siguiente_codigo())
            productos.append(nuevo)
            limpiar_campos()
            listar_productos()
            al_cambiar()
            messagebox.showinfo("Éxito", "Producto publicado correctamente.", parent=ventana)
        except ValueError:
            messagebox.showerror("Error", "Precio y Stock deben ser numéricos.", parent=ventana)

    def texto_producto(p):
        return f"ID: {p.codigo} | {p.nombre} - C${p.precio:.2f} | Cat: {p.categoria} | Stock: {p.stock}"

    def listar_productos():
        lista_visual.delete(0, tk.END)
        visibles[:] = productos
        for p in productos:
            lista_visual.insert(tk.END, texto_producto(p))

    def actualizar_producto():
        seleccion = lista_visual.curselection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Seleccione un producto de la lista.", parent=ventana)
            return

        indice = seleccion[0]
        nombre = entry_nombre.get().strip()
        precio = entry_precio.get().strip()
        categoria = entry_categoria.get().strip()
        stock = entry_stock.get().strip()
        descripcion = entry_descripcion.get().strip()

        if not nombre or not precio or not categoria or not stock or not descripcion:
            messagebox.showwarning("Aviso", "Todos los campos son obligatorios.", parent=ventana)
            return

        try:
            # Primero se convierten los números; si alguno falla, no se modifica nada
            nuevo_precio = float(precio)
            nuevo_stock = int(stock)
            if nuevo_precio < 0:
                messagebox.showerror("Error", "El precio no puede ser negativo.", parent=ventana)
                return
            if nuevo_stock < 0:
                messagebox.showerror("Error", "El stock no puede ser negativo.", parent=ventana)
                return
            p = visibles[indice]
            p.nombre = nombre
            p.precio = nuevo_precio
            p.categoria = categoria
            p.stock = nuevo_stock
            p.descripcion = descripcion
            limpiar_campos()
            listar_productos()
            al_cambiar()
            messagebox.showinfo("Éxito", "Producto actualizado.", parent=ventana)
        except ValueError:
            messagebox.showerror("Error", "Verifique que el precio y stock sean válidos.", parent=ventana)

    def eliminar_producto():
        seleccion = lista_visual.curselection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Seleccione un producto para eliminar.", parent=ventana)
            return

        indice = seleccion[0]
        productos.remove(visibles[indice])
        limpiar_campos()
        listar_productos()
        al_cambiar()
        messagebox.showinfo("Éxito", "Producto eliminado.", parent=ventana)

    def seleccionar_producto(event):
        seleccion = lista_visual.curselection()
        if seleccion:
            p = visibles[seleccion[0]]
            limpiar_campos()
            entry_nombre.insert(0, p.nombre)
            entry_precio.insert(0, str(p.precio))
            entry_categoria.insert(0, p.categoria)
            entry_stock.insert(0, str(p.stock))
            entry_descripcion.insert(0, p.descripcion)

    def limpiar_campos():
        entry_nombre.delete(0, tk.END)
        entry_precio.delete(0, tk.END)
        entry_categoria.delete(0, tk.END)
        entry_stock.delete(0, tk.END)
        entry_descripcion.delete(0, tk.END)

    def buscar_producto():
        texto_buscado = entry_busqueda.get().strip().lower()
        lista_visual.delete(0, tk.END)
        if not texto_buscado:
            listar_productos()
            return

        encontrados = [p for p in productos if texto_buscado in p.nombre.lower() or texto_buscado in p.categoria.lower()]
        visibles[:] = encontrados
        for p in encontrados:
            lista_visual.insert(tk.END, texto_producto(p))

    # --- VENTANA DE GESTION (DISEÑO EXACTO NUVIX) ---
    # Fondo gris claro suave de la aplicación web por detrás
    ventana.config(bg="#e8ecef")

    # Contenedor tipo Tarjeta Modal (Blanco puro como en tus capturas)
    main_card = tk.Frame(ventana, bg="#ffffff", padx=25, pady=20)
    main_card.pack(fill="both", expand=True, padx=20, pady=20)

    # --- ENCABEZADO CON LOGO DE DOS TONOS (Nuvix) ---
    brand_frame = tk.Frame(main_card, bg="#ffffff", height=45)
    brand_frame.pack(anchor="w", fill="x")

    # "Nuv" en verde oscuro
    tk.Label(brand_frame, text="Nu", font=("Segoe UI", 24, "bold"), fg="#0b3c3d", bg="#ffffff").place(x=0, y=0)
    # "ix" en turquesa colocado justo al lado (ajusta el valor de x si quieres acercarlo o alejarlo más)
    tk.Label(brand_frame, text="vix", font=("Segoe UI", 24, "bold"), fg="#00acc1", bg="#ffffff").place(x=45, y=0)

    lbl_title = tk.Label(main_card, text="Administración de Productos", font=("Segoe UI", 13, "bold"), fg="#222222", bg="#ffffff")
    # Usamos un pequeño espacio arriba (pady) para que el título no se encime con el logo debido al place
    lbl_title.pack(anchor="w", pady=(35, 15))

    # Campos del Formulario
    def crear_campo(parent, label_text):
        lbl = tk.Label(parent, text=label_text, font=("Segoe UI", 10), fg="#666666", bg="#ffffff")
        lbl.pack(anchor="w", pady=(4, 2))
        entry = tk.Entry(parent, font=("Segoe UI", 11), width=42, relief="solid", bd=1)
        entry.pack(anchor="w", pady=(0, 8))
        return entry

    entry_nombre = crear_campo(main_card, "Nombre del producto")
    entry_precio = crear_campo(main_card, "Precio")
    entry_categoria = crear_campo(main_card, "Categoría")
    entry_stock = crear_campo(main_card, "Stock disponible")
    entry_descripcion = crear_campo(main_card, "Descripción")   # es el texto que se ve en la tarjeta de la tienda

    # Botones de Acción (Verde azulado oscuro idéntico a tus botones de "Iniciar sesión" / "Crear cuenta": #0b3c3d o #083334)
    btn_frame = tk.Frame(main_card, bg="#ffffff")
    btn_frame.pack(pady=10)

    btn_estilo = {
        "font": ("Segoe UI", 10, "bold"),
        "fg": "white",
        "bg": "#083334",              # Tono verde azulado oscuro idéntico al de tus botones
        "activebackground": "#052223",
        "activeforeground": "white",
        "relief": "flat",
        "padx": 12,
        "pady": 8
    }

    tk.Button(btn_frame, text="Publicar", command=crear_producto, **btn_estilo).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="Actualizar", command=actualizar_producto, **btn_estilo).grid(row=0, column=1, padx=5)
    tk.Button(btn_frame, text="Eliminar", command=eliminar_producto, **btn_estilo).grid(row=0, column=2, padx=5)

    # Buscador y Lista de Resultados
    search_frame = tk.Frame(main_card, bg="#ffffff")
    search_frame.pack(fill="x", pady=5)

    tk.Label(search_frame, text="Buscar:", font=("Segoe UI", 9), fg="#666666", bg="#ffffff").pack(side="left", padx=(0, 5))
    entry_busqueda = tk.Entry(search_frame, font=("Segoe UI", 10), width=20, relief="solid", bd=1)
    entry_busqueda.pack(side="left", padx=5)
    tk.Button(search_frame, text="Buscar", command=buscar_producto, font=("Segoe UI", 9, "bold"), fg="white", bg="#00acc1", relief="flat", padx=10, pady=4).pack(side="left", padx=5)

    # exportselection=False: sin esto la lista pierde la selección al hacer clic/seleccionar texto en un Entry
    lista_frame = tk.Frame(main_card, bg="#ffffff")
    lista_frame.pack(pady=10)
    lista_visual = tk.Listbox(lista_frame, font=("Segoe UI", 9), width=58, height=6, relief="solid", bd=1, exportselection=False)
    lista_visual.pack()
    # Barra de desplazamiento horizontal para ver el texto completo del producto
    scroll_x = tk.Scrollbar(lista_frame, orient="horizontal", command=lista_visual.xview)
    scroll_x.pack(fill="x")
    lista_visual.config(xscrollcommand=scroll_x.set)
    lista_visual.bind("<<ListboxSelect>>", seleccionar_producto)

    # Muestra los productos que ya existen en la tienda
    listar_productos()
