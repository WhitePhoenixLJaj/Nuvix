import tkinter as tk
from funciones import cargar_imagen
from modelos import Usuario
from datos import USUARIOS, CLAVES

COLOR_BARRA = "#DBF9F3"
COLOR_PRIMARIO = "#075055"
COLOR_ERROR = "#C0392B"
COLOR_BORDE = "#BFC9C7"
FUENTE = "ABeeZee"

_ventana_abierta = None   # solo una pantalla de sesion a la vez


# ------------------------------------------------- logica (usa las listas)
def _buscar(identificador):
    """Devuelve la posicion en USUARIOS del usuario o correo dado, o -1."""
    identificador = identificador.strip().lower()
    for i in range(len(USUARIOS)):
        if identificador in (USUARIOS[i].nombre_usuario.lower(),
                             USUARIOS[i].correo_electronico.lower()):
            return i
    return -1


def _iniciar_sesion(identificador, clave):
    """Devuelve el Usuario si los datos son correctos; si no, lanza ValueError."""
    if identificador.strip() == "" or clave == "":
        raise ValueError("Escribe tu usuario y tu contrasena.")
    i = _buscar(identificador)
    if i == -1 or CLAVES[i] != clave:
        raise ValueError("Usuario o contrasena incorrectos.")
    return USUARIOS[i]


def _registrar(usuario, clave, confirmacion):
    """Valida y agrega el usuario a las listas; si algo falla, lanza ValueError."""
    if (usuario.nombre.strip() == "" or usuario.apellido.strip() == ""
            or usuario.nombre_usuario.strip() == ""
            or usuario.correo_electronico.strip() == ""
            or usuario.telefono.strip() == "" or clave == ""):
        raise ValueError("Completa todos los campos.")
    if "@" not in usuario.correo_electronico or "." not in usuario.correo_electronico:
        raise ValueError("El correo electronico no es valido.")
    if not usuario.telefono.replace(" ", "").replace("-", "").isdigit():
        raise ValueError("El telefono solo debe tener numeros.")
    if len(clave) < 6:
        raise ValueError("La contrasena debe tener al menos 6 caracteres.")
    if clave != confirmacion:
        raise ValueError("Las contrasenas no coinciden.")
    if _buscar(usuario.nombre_usuario) != -1:
        raise ValueError("Ese nombre de usuario ya esta en uso.")
    if _buscar(usuario.correo_electronico) != -1:
        raise ValueError("Ese correo ya tiene una cuenta.")
    USUARIOS.append(usuario)
    CLAVES.append(clave)


# ------------------------------------------------------------------ piezas
def _crear_ventana(principal, titulo, ancho, alto):
    """Ventana emergente centrada sobre la principal, con el logo arriba."""
    global _ventana_abierta
    if _ventana_abierta is not None and _ventana_abierta.winfo_exists():
        _ventana_abierta.destroy()

    v = tk.Toplevel(principal)
    _ventana_abierta = v
    v.title(titulo)
    v.resizable(False, False)
    v.configure(bg="#FFFFFF")
    v.transient(principal)

    x = principal.winfo_x() + (principal.winfo_width() - ancho) // 2
    y = principal.winfo_y() + (principal.winfo_height() - alto) // 2
    v.geometry(f"{ancho}x{alto}+{max(x, 0)}+{max(y, 0)}")

    cabecera = tk.Frame(v, bg=COLOR_BARRA, height=79)
    cabecera.pack(fill="x")
    cabecera.pack_propagate(False)
    logo = cargar_imagen(ruta_imagen="gui/imagenes/logo.png", ancho=235, alto=59)
    etiqueta_logo = tk.Label(cabecera, image=logo, bg=COLOR_BARRA, bd=0)
    etiqueta_logo.image = logo   # sin esto Python borra la imagen
    etiqueta_logo.pack(expand=True)

    try:
        v.wait_visibility()
        v.grab_set()             # bloquea la ventana principal mientras esta abierta
    except tk.TclError:
        pass
    return v


def _campo(padre, texto, oculto=False):
    """Etiqueta + caja de texto. Devuelve (contenedor, entry)."""
    marco = tk.Frame(padre, bg="#FFFFFF")
    tk.Label(marco, text=texto, bg="#FFFFFF", fg="#333333", anchor="w",
             font=(FUENTE, -14)).pack(fill="x", pady=(10, 2))
    entry = tk.Entry(
        marco,
        font=(FUENTE, -16),
        bd=0,
        relief="flat",
        highlightthickness=1,
        highlightbackground=COLOR_BORDE,
        highlightcolor=COLOR_PRIMARIO,
        show="*" if oculto else "")
    entry.pack(fill="x", ipady=6)
    return marco, entry


def _boton_principal(padre, texto, comando):
    return tk.Button(
        padre,
        text=texto,
        command=comando,
        bg=COLOR_PRIMARIO,
        fg="#FFFFFF",
        activebackground="#053b3f",
        activeforeground="#FFFFFF",
        bd=0,
        relief="flat",
        highlightthickness=0,
        cursor="hand2",
        font=(FUENTE, -18, "bold"))


def _mostrar_contrasena(padre, entradas):
    """Casilla para ver u ocultar las contrasenas."""
    visible = tk.BooleanVar(value=False)

    def alternar():
        for e in entradas:
            e.config(show="" if visible.get() else "*")

    tk.Checkbutton(padre, text="Mostrar contrasena", variable=visible,
                   command=alternar, bg="#FFFFFF", activebackground="#FFFFFF",
                   bd=0, highlightthickness=0, cursor="hand2",
                   font=(FUENTE, -13)).pack(anchor="w", pady=(8, 0))


def _enlace(padre, pregunta, texto_boton, comando):
    """Linea inferior: 'No tienes cuenta? Crear cuenta'."""
    fila = tk.Frame(padre, bg="#FFFFFF")
    tk.Label(fila, text=pregunta, bg="#FFFFFF", fg="#555555",
             font=(FUENTE, -14)).pack(side="left")
    tk.Button(fila, text=texto_boton, command=comando, bd=0, relief="flat",
              highlightthickness=0, bg="#FFFFFF", activebackground="#FFFFFF",
              fg=COLOR_PRIMARIO, cursor="hand2",
              font=(FUENTE, -14, "bold")).pack(side="left", padx=(4, 0))
    return fila


# --------------------------------------------------------- inicio de sesion
def abrir_inicio_sesion(principal, al_iniciar, ir_a_registro):
    """al_iniciar(usuario) se llama cuando el login es correcto.
    ir_a_registro() se llama si la persona pulsa 'Crear cuenta'."""
    v = _crear_ventana(principal, "Iniciar sesion", 440, 500)

    cuerpo = tk.Frame(v, bg="#FFFFFF")
    cuerpo.pack(fill="both", expand=True, padx=40, pady=(20, 20))

    tk.Label(cuerpo, text="Iniciar sesion", bg="#FFFFFF", fg=COLOR_PRIMARIO,
             font=(FUENTE, -28, "bold")).pack(anchor="w")

    marco_usuario, e_usuario = _campo(cuerpo, "Usuario o correo electronico")
    marco_usuario.pack(fill="x")
    marco_clave, e_clave = _campo(cuerpo, "Contrasena", oculto=True)
    marco_clave.pack(fill="x")
    _mostrar_contrasena(cuerpo, [e_clave])

    error = tk.Label(cuerpo, text="", bg="#FFFFFF", fg=COLOR_ERROR,
                     wraplength=360, justify="left", anchor="w",
                     font=(FUENTE, -13))
    error.pack(fill="x", pady=(10, 0))

    def enviar(_evento=None):
        try:
            usuario = _iniciar_sesion(e_usuario.get(), e_clave.get())
        except ValueError as problema:
            error.config(text=str(problema))
            return
        v.destroy()
        al_iniciar(usuario)

    _boton_principal(cuerpo, "Iniciar sesion", enviar).pack(fill="x", ipady=6, pady=(10, 0))

    def cambiar():
        v.destroy()
        ir_a_registro()

    _enlace(cuerpo, "No tienes cuenta?", "Crear cuenta", cambiar).pack(pady=(14, 0))

    v.bind("<Return>", enviar)
    v.bind("<Escape>", lambda e: v.destroy())
    e_usuario.focus_set()


# ----------------------------------------------------------------- registro
def abrir_registro(principal, al_iniciar, ir_a_inicio_sesion):
    """al_iniciar(usuario) se llama cuando la cuenta se crea (queda con la sesion abierta).
    ir_a_inicio_sesion() se llama si la persona pulsa 'Iniciar sesion'."""
    v = _crear_ventana(principal, "Crear cuenta", 480, 690)

    cuerpo = tk.Frame(v, bg="#FFFFFF")
    cuerpo.pack(fill="both", expand=True, padx=40, pady=(14, 16))

    tk.Label(cuerpo, text="Crear cuenta", bg="#FFFFFF", fg=COLOR_PRIMARIO,
             font=(FUENTE, -28, "bold")).pack(anchor="w")

    # nombre y apellido lado a lado para ahorrar espacio
    fila = tk.Frame(cuerpo, bg="#FFFFFF")
    fila.pack(fill="x")
    fila.columnconfigure(0, weight=1, uniform="mitad")
    fila.columnconfigure(1, weight=1, uniform="mitad")
    marco_nombre, e_nombre = _campo(fila, "Nombre")
    marco_nombre.grid(row=0, column=0, sticky="ew", padx=(0, 6))
    marco_apellido, e_apellido = _campo(fila, "Apellido")
    marco_apellido.grid(row=0, column=1, sticky="ew", padx=(6, 0))

    marco, e_usuario = _campo(cuerpo, "Nombre de usuario")
    marco.pack(fill="x")
    marco, e_correo = _campo(cuerpo, "Correo electronico")
    marco.pack(fill="x")
    marco, e_telefono = _campo(cuerpo, "Telefono")
    marco.pack(fill="x")
    marco, e_clave = _campo(cuerpo, "Contrasena (minimo 6 caracteres)", oculto=True)
    marco.pack(fill="x")
    marco, e_confirmar = _campo(cuerpo, "Confirmar contrasena", oculto=True)
    marco.pack(fill="x")
    _mostrar_contrasena(cuerpo, [e_clave, e_confirmar])

    error = tk.Label(cuerpo, text="", bg="#FFFFFF", fg=COLOR_ERROR,
                     wraplength=400, justify="left", anchor="w",
                     font=(FUENTE, -13))
    error.pack(fill="x", pady=(8, 0))

    def enviar(_evento=None):
        usuario = Usuario(
            nombre=e_nombre.get(),
            apellido=e_apellido.get(),
            nombre_usuario=e_usuario.get(),
            correo_electronico=e_correo.get(),
            telefono=e_telefono.get())
        try:
            _registrar(usuario, e_clave.get(), e_confirmar.get())
        except ValueError as problema:
            error.config(text=str(problema))
            return
        v.destroy()
        al_iniciar(usuario)

    _boton_principal(cuerpo, "Crear cuenta", enviar).pack(fill="x", ipady=6, pady=(8, 0))

    def cambiar():
        v.destroy()
        ir_a_inicio_sesion()

    _enlace(cuerpo, "Ya tienes cuenta?", "Iniciar sesion", cambiar).pack(pady=(12, 0))

    v.bind("<Return>", enviar)
    v.bind("<Escape>", lambda e: v.destroy())
    e_nombre.focus_set()
