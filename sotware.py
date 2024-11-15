import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import json
import os

# Archivos JSON
EMPLOYEES_FILE = "empleados.json"
INVENTORY_FILE = "inventario.json"

# Funciones para manejar archivos JSON
def cargar_empleados():
    if os.path.exists(EMPLOYEES_FILE):
        with open(EMPLOYEES_FILE, 'r') as f:
            return json.load(f)
    return {}

def guardar_empleados(data):
    with open(EMPLOYEES_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Función para aplicar imagen de fondo a las ventanas
def aplicar_fondo(ventana, ruta_imagen="el desembarco.jpg"):
    try:
        background_image = Image.open(ruta_imagen)
        background_image = background_image.resize((600, 400), Image.Resampling.LANCZOS)
        bg_image = ImageTk.PhotoImage(background_image)
        bg_label = tk.Label(ventana, image=bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        ventana.bg_image = bg_image
    except Exception as e:
        print(f"Error al cargar la imagen de fondo: {e}")

# Clase Principal de la Aplicación
class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión")
        self.root.geometry("600x400")
        aplicar_fondo(self.root)
        
        self.label_bienvenida = tk.Label(
            root, 
            text="Bienvenido al Sistema de Gestión", 
            font=("Arial", 18), 
            bg="#ffffff", 
            fg="#333333"
        )
        self.label_bienvenida.pack(pady=20)
        
        self.boton_login = tk.Button(
            root, 
            text="Iniciar Sesión", 
            command=self.mostrar_login, 
            bg="#4CAF50", 
            fg="white", 
            font=("Arial", 14), 
            width=15, 
            height=2
        )
        self.boton_login.pack(pady=10)

    def mostrar_login(self):
        if self.root.winfo_exists():
            self.root.withdraw()
        self.ventana_login = tk.Toplevel(self.root)
        self.ventana_login.title("Login")
        self.ventana_login.geometry("300x250")
        aplicar_fondo(self.ventana_login)

        self.label_usuario = tk.Label(self.ventana_login, text="Usuario", font=("Arial", 12))
        self.label_usuario.pack(pady=5)
        self.entrada_usuario = tk.Entry(self.ventana_login, font=("Arial", 12))
        self.entrada_usuario.pack()

        self.label_contraseña = tk.Label(self.ventana_login, text="Contraseña", font=("Arial", 12))
        self.label_contraseña.pack(pady=5)
        self.entrada_contraseña = tk.Entry(self.ventana_login, show="*", font=("Arial", 12))
        self.entrada_contraseña.pack()

        self.boton_iniciar = tk.Button(
            self.ventana_login, 
            text="Iniciar", 
            command=self.login, 
            bg="#2196F3", 
            fg="white", 
            font=("Arial", 12), 
            width=10
        )
        self.boton_iniciar.pack(pady=20)

        self.boton_volver = tk.Button(
            self.ventana_login, 
            text="Volver Atrás", 
            command=self.volver_principal, 
            bg="#F44336", 
            fg="white", 
            font=("Arial", 12), 
            width=10
        )
        self.boton_volver.pack()

    def volver_principal(self):
        if hasattr(self, 'ventana_login') and self.ventana_login.winfo_exists():
            self.ventana_login.destroy()
        self.root.deiconify()

    def login(self):
        usuario = self.entrada_usuario.get()
        contraseña = self.entrada_contraseña.get()
        
        empleados = cargar_empleados()
        
        if usuario == "dueño" and contraseña == "dueño123":
            self.mostrar_panel_dueño()
        elif usuario in empleados and empleados[usuario]["contraseña"] == contraseña:
            self.mostrar_seleccion_rol(usuario)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrecta")

    def mostrar_seleccion_rol(self, usuario):
        roles = ["cajero", "encargado_stock"]
        self.ventana_login.withdraw()
        self.ventana_rol = tk.Toplevel(self.root)
        self.ventana_rol.title("Seleccionar Rol")
        self.ventana_rol.geometry("300x200")
        aplicar_fondo(self.ventana_rol)

        tk.Label(self.ventana_rol, text="Selecciona tu rol", font=("Arial", 12)).pack(pady=10)
        
        self.combo_rol = ttk.Combobox(self.ventana_rol, values=roles, font=("Arial", 12))
        self.combo_rol.pack(pady=10)

        self.boton_continuar = tk.Button(
            self.ventana_rol, 
            text="Continuar", 
            command=lambda: self.iniciar_con_rol(usuario), 
            bg="#4CAF50", 
            fg="white", 
            font=("Arial", 12), 
            width=10
        )
        self.boton_continuar.pack(pady=10)

    def iniciar_con_rol(self, usuario):
        rol_seleccionado = self.combo_rol.get()
        if rol_seleccionado == "cajero":
            self.mostrar_panel_cajero()
        elif rol_seleccionado == "encargado_stock":
            self.mostrar_panel_stock()

    def mostrar_panel_dueño(self):
        if hasattr(self, 'ventana_login') and self.ventana_login.winfo_exists():
            self.ventana_login.destroy()
        
        self.ventana_dueño = tk.Toplevel(self.root)
        self.ventana_dueño.title("Panel del Dueño")
        self.ventana_dueño.geometry("300x300")
        aplicar_fondo(self.ventana_dueño)

        self.boton_crear_cuenta = tk.Button(
            self.ventana_dueño, 
            text="Crear Cuenta Empleado", 
            command=self.crear_cuenta_empleado, 
            bg="#FF5722", 
            fg="white", 
            font=("Arial", 12), 
            width=20, 
            height=2
        )
        self.boton_crear_cuenta.pack(pady=10)

        self.boton_modificar_sueldo = tk.Button(
            self.ventana_dueño, 
            text="Modificar Sueldo", 
            command=self.mostrar_empleados_para_modificar_sueldo, 
            bg="#FF9800", 
            fg="white", 
            font=("Arial", 12), 
            width=20, 
            height=2
        )
        self.boton_modificar_sueldo.pack(pady=10)

        self.boton_despedir_empleado = tk.Button(
            self.ventana_dueño, 
            text="Despedir Empleado", 
            command=self.mostrar_empleados_para_despedir, 
            bg="#F44336", 
            fg="white", 
            font=("Arial", 12), 
            width=20, 
            height=2
        )
        self.boton_despedir_empleado.pack(pady=10)

    def crear_cuenta_empleado(self):
        self.ventana_dueño.withdraw()
        ventana_crear = tk.Toplevel(self.ventana_dueño)
        ventana_crear.title("Crear Cuenta Empleado")
        ventana_crear.geometry("300x300")
        aplicar_fondo(ventana_crear)
        
        tk.Label(ventana_crear, text="Nombre de usuario", font=("Arial", 12)).pack(pady=5)
        entrada_usuario = tk.Entry(ventana_crear, font=("Arial", 12))
        entrada_usuario.pack()

        tk.Label(ventana_crear, text="Contraseña", font=("Arial", 12)).pack(pady=5)
        entrada_contraseña = tk.Entry(ventana_crear, font=("Arial", 12))
        entrada_contraseña.pack()

        tk.Label(ventana_crear, text="Rol", font=("Arial", 12)).pack(pady=5)
        combo_rol = ttk.Combobox(ventana_crear, values=["cajero", "encargado_stock"], font=("Arial", 12))
        combo_rol.pack()

        tk.Label(ventana_crear, text="Sueldo", font=("Arial", 12)).pack(pady=5)
        entrada_sueldo = tk.Entry(ventana_crear, font=("Arial", 12))
        entrada_sueldo.pack()

        def guardar():
            usuario = entrada_usuario.get()
            contraseña = entrada_contraseña.get()
            rol = combo_rol.get()
            sueldo = entrada_sueldo.get()

            if not all([usuario, contraseña, rol, sueldo]):
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return

            try:
                sueldo = float(sueldo)
                if sueldo <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "El sueldo debe ser un número válido mayor a 0.")
                return

            empleados = cargar_empleados()
            if usuario in empleados:
                messagebox.showerror("Error", "El usuario ya existe.")
                return

            empleados[usuario] = {"contraseña": contraseña, "rol": rol, "sueldo": sueldo}
            guardar_empleados(empleados)
            messagebox.showinfo("Éxito", f"Cuenta de {rol} creada con éxito.")
            ventana_crear.destroy()
            self.ventana_dueño.deiconify()

        boton_guardar = tk.Button(
            ventana_crear, 
            text="Guardar", 
            command=guardar, 
            bg="#4CAF50", 
            fg="white", 
            font=("Arial", 12), 
            width=10
        )
        boton_guardar.pack(pady=10)

        boton_volver = tk.Button(
            ventana_crear, 
            text="Volver", 
            command=lambda: [ventana_crear.destroy(), self.ventana_dueño.deiconify()], 
            bg="#F44336", 
            fg="white", 
            font=("Arial", 12), 
            width=10
        )
        boton_volver.pack(pady=5)

    def mostrar_empleados_para_modificar_sueldo(self):
        empleados = cargar_empleados()
        
        if not empleados:
            messagebox.showinfo("Sin empleados", "No hay empleados para modificar sueldos.")
            return
        
        self.ventana_dueño.withdraw()
        
        self.ventana_modificar_sueldo = tk.Toplevel(self.ventana_dueño)
        self.ventana_modificar_sueldo.title("Modificar Sueldo")
        self.ventana_modificar_sueldo.geometry("300x400")
        
        aplicar_fondo(self.ventana_modificar_sueldo)
        
        tk.Label(
            self.ventana_modificar_sueldo, 
            text="Selecciona un empleado", 
            font=("Arial", 12)
        ).pack(pady=10)
        
        frame_empleados = tk.Frame(self.ventana_modificar_sueldo)
        frame_empleados.pack(pady=10)
        
        for empleado in empleados:
            if empleado != "dueño":
                boton_empleado = tk.Button(
                    frame_empleados,
                    text=f"{empleado} - Sueldo actual: ${empleados[empleado]['sueldo']}",
                    command=lambda emp=empleado: self.modificar_sueldo(emp, self.ventana_modificar_sueldo),
                    bg="#2196F3",
                    fg="white",
                    font=("Arial", 12),
                    width=30
                )
                boton_empleado.pack(pady=5)
        
        tk.Button(
            self.ventana_modificar_sueldo,
            text="Volver al Panel",
            command=self.volver_panel_dueño,
            bg="#F44336",
            fg="white",
            font=("Arial", 12),
            width=15
        ).pack(pady=20)

    def volver_panel_dueño(self):
        for widget in self.ventana_dueño.winfo_children():
            if isinstance(widget, tk.Toplevel):
                widget.destroy()
        self.ventana_dueño.deiconify()

    def modificar_sueldo(self, empleado, ventana_padre):
        empleados = cargar_empleados()
        sueldo_actual = empleados[empleado]['sueldo']
        
        ventana_sueldo = tk.Toplevel(ventana_padre)
        ventana_sueldo.title(f"Modificar Sueldo - {empleado}")
        ventana_sueldo.geometry("400x300")
        
        aplicar_fondo(ventana_sueldo)
        
        frame = tk.Frame(ventana_sueldo, bg='white')
        frame.pack(pady=20)
        
        tk.Label(
            frame,
            text=f"Empleado: {empleado}",
            font=("Arial", 14, "bold"),
            bg='white'
        ).pack(pady=5)
        
        tk.Label(
            frame,
            text=f"Sueldo actual: ${sueldo_actual}",
            font=("Arial", 12),
            bg='white'
        ).pack(pady=5)
        
        tk.Label(
            frame,
            text="Nuevo sueldo:",
            font=("Arial", 12),
            bg='white'
        ).pack(pady=5)
        
        entrada_sueldo = tk.Entry(frame, font=("Arial", 12))
        entrada_sueldo.pack(pady=10)
        entrada_sueldo.insert(0, str(sueldo_actual))

        