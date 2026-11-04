import tkinter as tk
from tkinter import messagebox
from funciones import cargar_imagen
from datos import PRODUCTOS
from gui.productos import crear_galeria
from gui.sesion import abrir_inicio_sesion, abrir_registro
from gui.gestion import abrir_gestion
#creacion de la ventana principal

def ventana_principal():
    principal = tk.Tk()
    principal.title("Nuvix")
    usuario_actual = None   # None = nadie ha iniciado sesion todavia
    alto_ventana = min(1024, principal.winfo_screenheight() - 90)
    principal.geometry(f"1440x{alto_ventana}")
    principal.resizable(False,False)

    #menu principal
    inicio = tk.Canvas(
        principal,
        width=1440,
        height=alto_ventana,
        bd=0,
        highlightthickness=0,
        bg="#FFFFFF")
    inicio.place(x=0,y=0)
    #-------------productos------------
    galeria = crear_galeria(principal, PRODUCTOS, x=0, y=135,
                  al_hacer_clic=lambda p: print("Producto:", p.nombre))

    #-------------Barra de menu principal------------
    barra = tk.Canvas(
        principal,
        width=1440,
        height=82,
        bd=0,
        bg="#DBF9F3")
    barra.place(x=0,y=0)
    #-------------logo--------------------------
    logo = cargar_imagen(ruta_imagen="gui/imagenes/logo.png",ancho=313, alto=79)
    barra.create_image(0,3, image = logo, anchor = "nw")
    #-------------barra de busqueda---------------
    barra_busqueda_entry = tk.Entry(
        principal,
        bg="#FFFFFF",
        bd=0,
        relief="flat",
        font=("ABeeZee",-16),
    )
    barra.create_window(428,31, window=barra_busqueda_entry, anchor="nw", width=400)
    barra_busqueda = cargar_imagen(ruta_imagen="gui/imagenes/barra_busqueda.png", ancho=508,alto=53)
    imagen_busqueda = barra.create_image(404,15, image = barra_busqueda, anchor = "nw")

    def buscar_producto(evento=None):
        galeria.buscar(barra_busqueda_entry.get())

    # Enter dentro de la caja de texto busca
    barra_busqueda_entry.bind("<Return>", buscar_producto)

    # la lupa (extremo derecho de la imagen) tambien busca al hacer clic
    def sobre_lupa(evento):
        return evento.x >= 404 + 508 - 60

    def clic_barra(evento):
        if sobre_lupa(evento):
            buscar_producto()
        else:
            barra_busqueda_entry.focus_set()

    barra.tag_bind(imagen_busqueda, "<Button-1>", clic_barra)
    barra.tag_bind(imagen_busqueda, "<Motion>",
                   lambda e: barra.config(cursor="hand2" if sobre_lupa(e) else ""))
    barra.tag_bind(imagen_busqueda, "<Leave>", lambda e: barra.config(cursor=""))
    #-------------boton iniciar sesion-------------
    iniciar_sesion = tk.Button(
        principal,
        text="Iniciar sesion",
        font=("ABeeZee",-24,"normal"),
        command=lambda:mostrar_login(),
        bd=0,
        relief="flat",
        highlightthickness=0,
        activebackground="#DBF9F3",
        bg="#DBF9F3")
    barra.create_window(978,20, window=iniciar_sesion,anchor="nw")
    icono_usuario = cargar_imagen(ruta_imagen="gui/imagenes/icono_usuario.png", ancho=32, alto=32)
    barra.create_image(944,25, image = icono_usuario, anchor = "nw")
    #------------boton de crear cuenta------------
    crear_cuenta = cargar_imagen(ruta_imagen="gui/imagenes/crear_cuenta.png", ancho=190, alto=50)
    boton_crear_cuenta = tk.Button(
        principal,
        command=lambda:mostrar_registro(),
        bd=0,
        relief="flat",
        highlightthickness=0,
        image=crear_cuenta,
        bg="#DBF9F3")
    barra.create_window(1153,20, window=boton_crear_cuenta, anchor = "nw")


    #---------------Boton de mas vendidos-----------------
    mas_vendidos = tk.Button(
        principal,
        command=lambda:print("Productos mas vendidos"),
        bd=0,
        relief="flat",
        highlightthickness=0,
        bg="#FFFFFF",
        text="Mas vendidos",
        font=("ABeeZee",-20,"normal"),
        activebackground="#FFFFFF")
    inicio.create_window(178,93, window=mas_vendidos, anchor="nw")
    #----------------boton de comprar de nuevo---------------
    comprar_de_nuevo = tk.Button(
        principal,
        command=lambda:print("Comprar producto de nuevo"),
        bd=0,
        relief="flat",
        highlightthickness=0,
        bg="#FFFFFF",
        text="Comprar de nuevo",
        font=("ABeeZee",-20,"normal"),
        activebackground="#FFFFFF")
    inicio.create_window(325,93, window=comprar_de_nuevo, anchor="nw")
    #------------------boton de vender-----------------------
    vender = tk.Button(
        principal,
        command=lambda:ir_a_vender(),
        bd=0,
        relief="flat",
        highlightthickness=0,
        bg="#FFFFFF",
        text="Vender",
        font=("ABeeZee",-20,"normal"),
        activebackground="#FFFFFF")
    inicio.create_window(518, 93, window=vender, anchor= "nw")
    #-------------------boton de acerca de-----------------
    acerca_de = tk.Button(
        principal,
        command=lambda:print("Acerca de"),
        bd=0,
        relief="flat",
        highlightthickness=0,
        bg="#FFFFFF",
        text="Acerca de ***",
        font=("ABeeZee",-20,"normal"),
        activebackground="#FFFFFF")
    inicio.create_window(899,93, window=acerca_de, anchor="nw")
    #--------------------Centro de ayuda-------------------
    ayuda = tk.Button(
        principal,
        command=lambda:print("Abrir centro de ayuda"),
        bd=0,
        relief="flat",
        highlightthickness=0,
        bg="#FFFFFF",
        text="Centro de ayuda",
        font=("ABeeZee",-20,"normal"),
        activebackground="#FFFFFF")
    inicio.create_window(1038,93, window=ayuda, anchor="nw")
    #--------------------boton de vende en-------------------
    vende_en = tk.Button(
        principal,
        command=lambda:print("boton de vende en"),
        bd=0,
        relief="flat",
        highlightthickness=0,
        bg="#FFFFFF",
        text="Vende en ***",
        font=("ABeeZee",-20,"normal"),
        activebackground="#FFFFFF")
    inicio.create_window(1223,93, window=vende_en, anchor="nw")
    #--------------------boton de categoria------------------
    boton_categoria = tk.Button(
        principal,
        command=lambda:print("abrir menu de categoria"),
        bd=0,
        relief="flat",
        highlightthickness=0,
        bg="#FFFFFF",
        text="Categorias",
        font=("ABeeZee",-20,"normal"),
        activebackground="#FFFFFF"
    )
    inicio.create_window(41,93, window=boton_categoria, anchor="nw")
    chevron_abajo = cargar_imagen(ruta_imagen="gui/imagenes/chevron_abajo.png",ancho=24,alto=24)
    inicio.create_image(151,98, image = chevron_abajo, anchor = "nw")
    
    #-------------pantallas de sesion------------
    def al_iniciar_sesion(usuario):
        nonlocal usuario_actual
        usuario_actual = usuario      # se recuerda quien inicio sesion
        messagebox.showinfo("Nuvix", f"Bienvenido, {usuario.nombre}!", parent=principal)

    def ir_a_vender():
        if usuario_actual is None:
            messagebox.showinfo(
                "Nuvix",
                "Para vender un producto primero debes iniciar sesion.",
                parent=principal)
            return
        abrir_gestion(principal, PRODUCTOS, galeria.refrescar)

    def mostrar_login():
        abrir_inicio_sesion(principal, al_iniciar_sesion, mostrar_registro)

    def mostrar_registro():
        abrir_registro(principal, al_iniciar_sesion, mostrar_login)

    principal.mainloop()
