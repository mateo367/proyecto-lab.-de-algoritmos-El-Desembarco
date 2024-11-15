import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import os
from collections import defaultdict

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

def cargar_inventario():
    if os.path.exists(INVENTORY_FILE):
        with open(INVENTORY_FILE, 'r') as f:
            return json.load(f)
    return []  # Devuelve una lista vacía si no hay inventario

def guardar_inventario(data):
    with open(INVENTORY_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Función para aplicar imagen de fondo a las ventanas
def aplicar_fondo(ventana, ruta_imagen="el desembarco.jpg"):
    try:
        # Cargar la imagen de fondo
        background_image = Image.open(ruta_imagen)
        background_image = background_image.resize((600, 400), Image.Resampling.LANCZOS)
        bg_image = ImageTk.PhotoImage(background_image)
        
        # Crear un Label con la imagen de fondo
        bg_label = tk.Label(ventana, image=bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Guardar la referencia de la imagen para evitar que se elimine
        ventana.bg_image = bg_image
    except Exception as e:
        print(f"Error al cargar la imagen de fondo: {e}")

# Clase Principal de la Aplicación
class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión")
        self.root.geometry("600x400")

        # Inicializar control_mesas para almacenar el estado de cada mesa
        self.control_mesas = {f"mesa{i}": tk.StringVar(value="Libre") for i in range(1, 9)}

        # Aplicar imagen de fondo a la ventana principal
        aplicar_fondo(self.root)
        
        # Bienvenida
        self.label_bienvenida = tk.Label(root, text="Bienvenido al Sistema de Gestión", font=("Arial", 18), bg="#ffffff", fg="#333333")
        self.label_bienvenida.pack(pady=20)
        
        # Botón para iniciar sesión
        self.boton_login = tk.Button(root, text="Iniciar Sesión", command=self.mostrar_login, bg="#4CAF50", fg="white", font=("Arial", 14), width=15, height=2)
        self.boton_login.pack(pady=10)

    def mostrar_login(self):
        self.root.withdraw()  # Oculta la ventana actual en lugar de destruirla para volver atrás
        
        # Nueva ventana de login
        self.ventana_login = tk.Toplevel(self.root)
        self.ventana_login.title("Login")
        self.ventana_login.geometry("600x400")
        
        
        
        # Aplicar imagen de fondo
        aplicar_fondo(self.ventana_login)
        
        # Campos de usuario y contraseña
        self.label_usuario = tk.Label(self.ventana_login, text="Usuario", font=("Arial", 12))
        self.label_usuario.pack(pady=5)
        self.entrada_usuario = tk.Entry(self.ventana_login, font=("Arial", 12))
        self.entrada_usuario.pack()

        self.label_contraseña = tk.Label(self.ventana_login, text="Contraseña", font=("Arial", 12))
        self.entrada_contraseña = tk.Entry(self.ventana_login, show="*", font=("Arial", 12))
        self.label_contraseña.pack(pady=5)
        self.entrada_contraseña.pack()

        # Botón de login
        self.boton_iniciar = tk.Button(self.ventana_login, text="Iniciar", command=self.login, bg="#2196F3", fg="white", font=("Arial", 12), width=10)
        self.boton_iniciar.pack(pady=20)

        # Botón para volver atrás
        self.boton_volver = tk.Button(self.ventana_login, text="Volver Atrás", command=self.volver_principal, bg="#F44336", fg="white", font=("Arial", 12), width=10)
        self.boton_volver.pack()


    def volver_principal(self):
        self.ventana_login.destroy()
        self.root.deiconify()  # Muestra la ventana principal de nuevo

    def login(self):
        usuario = self.entrada_usuario.get()
        contraseña = self.entrada_contraseña.get()
        
        empleados = cargar_empleados()
        
        # Verifica si es el dueño
        if usuario == "dueño" and contraseña == "dueño123":
            self.mostrar_panel_dueño()
        elif usuario in empleados and empleados[usuario]["contraseña"] == contraseña:
            rol = empleados[usuario]["rol"]
            if rol == "cajero":
                self.mostrar_panel_cajero()  # Asegúrate de que esta función esté definida
            elif rol == "encargado_stock":
                self.mostrar_panel_stock()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrecta")

    # Panel para el Dueño
    def mostrar_panel_dueño(self):
        self.ventana_login.destroy()  # Cierra la ventana de login
        
        self.ventana_dueño = tk.Toplevel(self.root)
        self.ventana_dueño.title("Panel del Dueño")
        self.ventana_dueño.geometry("600x400")
        
        # Aplicar imagen de fondo
        aplicar_fondo(self.ventana_dueño)
        
        # Botones del dueño
        self.boton_crear_cuenta = tk.Button(self.ventana_dueño, text="Crear Cuenta Empleado", command=self.crear_cuenta_empleado, bg="#FF5722", fg="white", font=("Arial", 12), width=20, height=2)
        self.boton_crear_cuenta.pack(pady=10)
        
        self.boton_modificar_sueldo = tk.Button(self.ventana_dueño, text="Modificar Sueldo", command=self.mostrar_empleados_para_modificar_sueldo, bg="#FF9800", fg="white", font=("Arial", 12), width=20, height=2)
        self.boton_modificar_sueldo.pack(pady=10)
        
        self.boton_despedir_empleado = tk.Button(self.ventana_dueño, text="Despedir Empleado", command=self.mostrar_empleados_para_despedir, bg="#F44336", fg="white", font=("Arial", 12), width=20, height=2)
        self.boton_despedir_empleado.pack(pady=10)

        # Botón para volver atrás
        self.boton_volver = tk.Button(self.ventana_dueño, text="Volver Atrás", command=self.volver_login, bg="#F44336", fg="white", font=("Arial", 12), width=10)
        self.boton_volver.pack()
    
    def mostrar_panel_cajero(self):
        self.ventana_login.withdraw()

        self.ventana_cajero = tk.Toplevel(self.root)
        self.ventana_cajero.title("Panel de Empleado")
        self.ventana_cajero.geometry("600x400")
        
        aplicar_fondo(self.ventana_cajero)

        self.boton_mesas = tk.Button(self.ventana_cajero, text="Mesas", bg="Red", fg="white", font=("Arial", 12),command=self.mostrar_mesas, width=20, height=2)
        self.boton_mesas.pack(pady=(70, 20))
        self.boton_pedidos = tk.Button(self.ventana_cajero, text="Pedidos", bg="Red", fg="white", font=("Arial", 12),command=self.mostrar_pedidos, width=20, height=2)
        self.boton_pedidos.pack(pady=20)
        self.boton_QR_Menu = tk.Button(self.ventana_cajero, text="QR MENU", bg="Red", fg="white", font=("Arial", 12), width=20, height=2)
        self.boton_QR_Menu.pack(pady=20)

        volver = tk.Button(self.ventana_cajero, text="Volver atrás", command=self.volver_login_empleado)
        volver.pack()

    def mostrar_mesas(self):
        self.ventana_cajero.withdraw()

        self.ventana_mesas = tk.Toplevel(self.root)
        self.ventana_mesas.title("Panel de Empleado")
        self.ventana_mesas.geometry("600x400")
        
        aplicar_fondo(self.ventana_mesas)

        # Crear los Checkbuttons con los estados iniciales y almacenarlos en control_mesas
        for i in range(1, 9):
            mesa_checkbutton = tk.Checkbutton(
                self.ventana_mesas,
                text=f"Mesa{i}",
                variable=self.control_mesas[f"mesa{i}"],
                onvalue="Ocupado",
                offvalue="Libre",
                width=30,
                height=5,
            )
            mesa_checkbutton.grid(row=(i-1)//2, column=(i-1)%2, padx=(60, 0) if i % 2 != 0 else 0, pady=(10, 0))
            mesa_checkbutton.deselect()

        volver = tk.Button(self.ventana_mesas, text="Volver atrás", command=self.volver_mesas)
        volver.grid(row=4, columnspan=2)

    def volver_mesas(self):
        self.ventana_mesas.withdraw()
        self.ventana_cajero.deiconify()

    def volver_pedidos(self):
        self.ventana_pedidos.withdraw()
        self.ventana_cajero.deiconify()
    
    def pedido(self, info_especifica):
        self.ventana_pedidos.withdraw()

        self.pedido_especifico = tk.Toplevel(self.root)
        self.pedido_especifico.title("Pedido")
        self.pedido_especifico.geometry("300x600")
        
        aplicar_fondo(self.pedido_especifico)
        
        

        info_pedido = tk.Label(self.pedido_especifico, text=info_especifica)
        info_pedido.pack()

        volver = tk.Button(self.pedido_especifico, text="Volver atrás", command=self.volver_info_pedidos)
        volver.pack()
    
    def volver_info_pedidos(self):
        self.ventana_pedidos.deiconify()
        self.pedido_especifico.destroy()

    def mostrar_pedidos(self):
        self.ventana_cajero.withdraw()

        self.ventana_pedidos = tk.Toplevel(self.root)
        self.ventana_pedidos.title("Panel de Empleado")
        self.ventana_pedidos.geometry("600x400")
        
        aplicar_fondo(self.ventana_pedidos)

        # Verificar el estado de cada mesa y habilitar o deshabilitar los botones de pedido
        for i in range(1, 9):
            info_pedido = f"info{i}"
            pedido_button = tk.Button(
                self.ventana_pedidos,
                text=f"Pedido{i}",
                command=lambda info=info_pedido: self.pedido(info),
                width=20,
                height=2,
            )
            pedido_button.grid(row=(i-1)//2, column=(i-1)%2)
            
            # Habilitar o deshabilitar el botón según el estado de la mesa
            if self.control_mesas[f"mesa{i}"].get() == "Libre":
                pedido_button.config(state="disabled")

        volver = tk.Button(self.ventana_pedidos, text="Volver atrás", command=self.volver_pedidos)
        volver.grid(row=4, columnspan=2)

    def mostrar_panel_stock(self):
        self.ventana_login.withdraw()

        self.ventana_stock = tk.Toplevel(self.root)
        self.ventana_stock.title("Panel de Actor de Stock")
        self.ventana_stock.geometry("600x400")
        
        aplicar_fondo(self.ventana_stock)

        self.boton_agregar_producto = tk.Button(self.ventana_stock, text="Agregar producto", command=self.agregar_producto)
        self.boton_agregar_producto.pack()
        self_boton_pedidos = tk.Button(self.ventana_stock, text="Pedidos", command=self.pedidos_stock)
        self_boton_pedidos.pack()

        volver = tk.Button(self.ventana_stock,text="Volver atrás", command=self.volver_login_stock)
        volver.pack()

    def volver_login_stock(self):
        self.ventana_stock.withdraw()
        self.entrada_usuario.delete(0, "end")
        self.entrada_contraseña.delete(0, "end")
        self.ventana_login.deiconify()
    
    def volver_login_empleado(self):
        self.ventana_cajero.withdraw()
        self.entrada_usuario.delete(0, "end")
        self.entrada_contraseña.delete(0, "end")
        self.ventana_login.deiconify()
    
    def agregar_producto(self):
        self.ventana_stock.withdraw()

        self.ventana_agregar_producto = tk.Toplevel(self.root)
        self.ventana_agregar_producto.title("Agregar Producto")
        self.ventana_agregar_producto.geometry("600x400")
        
        aplicar_fondo(self.ventana_agregar_producto)
        
        # Etiquetas y campos de entrada para nombre y precio del producto
        self.nombre = tk.Label(self.ventana_agregar_producto, text="Nombre del producto")
        self.nombre.pack(pady=10)
        self.nombre_entrada = tk.Entry(self.ventana_agregar_producto)
        self.nombre_entrada.pack(pady=10)

        self.precio = tk.Label(self.ventana_agregar_producto, text="Precio del producto")
        self.precio.pack(pady=10)
        self.precio_entrada = tk.Entry(self.ventana_agregar_producto)
        self.precio_entrada.pack(pady=10)

        # Botones para enviar el producto o volver atrás
        Enviar = tk.Button(self.ventana_agregar_producto, text="Enviar", command=self.guardar_producto_nuevo)
        Enviar.pack(pady=10)

        Volver = tk.Button(self.ventana_agregar_producto, text="Volver atrás", command=self.volver_panel_stock_productos)
        Volver.pack(pady=10)

    def guardar_producto_nuevo(self):
        nombre_producto = self.nombre_entrada.get()
        precio_producto = self.precio_entrada.get()

        # Validación de los datos de entrada
        if not nombre_producto or not precio_producto:
            messagebox.showerror("Error", "Por favor, ingrese un nombre y un precio para el producto.")
            return

        try:
            precio_producto = float(precio_producto)
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un valor numérico válido.")
            return

        # Cargar los productos actuales
        inventario = cargar_inventario()

        # Crear un nuevo producto y agregarlo al inventario
        nuevo_producto = {"nombre": nombre_producto, "precio": precio_producto}
        inventario.append(nuevo_producto)

        # Guardar el inventario actualizado
        guardar_inventario(inventario)

        # Mostrar mensaje de éxito
        messagebox.showinfo("Éxito", f"Producto '{nombre_producto}' agregado con éxito.")
        
        # Limpiar los campos de entrada
        self.nombre_entrada.delete(0, tk.END)
        self.precio_entrada.delete(0, tk.END)

    
    def pedidos_stock(self):
        self.ventana_stock.withdraw()

        self.pedidos = tk.Toplevel(self.root)
        self.pedidos.title("Panel de Actor de Stock")
        self.pedidos.geometry("600x400")
        
        aplicar_fondo(self.pedidos)

        realizar_pedido = tk.Button(self.pedidos, text="Hacer un pedido", command=self.Realizar_pedido)
        realizar_pedido.grid(row=0, columnspan=2)
        
        cantidad_de_pedidos = 1

        for i in range(1, (cantidad_de_pedidos+1)):
            info_pedido_stock = f"info{i}"
            pedido_button = tk.Button(
                self.pedidos,
                text=f"Pedido{i}",
                command=lambda info = info_pedido_stock: self.pedido_stock(info),
                width=20,
                height=2,
            )
            pedido_button.grid(row=((i-1)//2)+1, column=((i-1)%2)+1)
    
        volver = tk.Button(self.pedidos, text="Volver atrás", command=self.volver_panel_stock)
        volver.grid(row=cantidad_de_pedidos+1, columnspan=2)

    def Realizar_pedido(self):
        self.pedidos.withdraw()

        self.ventana_pedido_nuevo = tk.Toplevel(self.root)
        self.ventana_pedido_nuevo.title("Panel de Actor de Stock")
        self.ventana_pedido_nuevo.geometry("600x400")
        
        aplicar_fondo(self.ventana_pedido_nuevo)

        # Cargar productos del inventario
        inventario = cargar_inventario()

        # Usar un defaultdict para contar cuántas veces se ha agregado cada producto
        self.productos_seleccionados = defaultdict(int)

        # Función para agregar productos a la lista
        def agregar_producto_a_lista(producto):
            self.productos_seleccionados[producto['nombre']] += 1
            messagebox.showinfo("Producto Agregado", f"Producto '{producto['nombre']}' agregado al pedido.")

        # Crear un botón por cada producto
        for i, producto in enumerate(inventario):
            nombre_producto = producto['nombre']
            precio_producto = producto['precio']
            
            # Crear un botón para cada producto
            boton_producto = tk.Button(
                self.ventana_pedido_nuevo,
                text=f"{nombre_producto} - ${precio_producto}",
                command=lambda p=producto: agregar_producto_a_lista(p),  # Pasamos el producto como argumento
                width=30,
                height=2
            )
            boton_producto.pack(pady=10)

        # Función para mostrar los productos seleccionados
        def mostrar_productos_seleccionados():
            if self.productos_seleccionados:
                productos_str = ""
                total = 0.0
                for nombre, cantidad in self.productos_seleccionados.items():
                    # Buscar el precio del producto en el inventario
                    producto = next(p for p in inventario if p['nombre'] == nombre)
                    precio_producto = producto['precio']
                    subtotal = precio_producto * cantidad
                    productos_str += f"{nombre} - {cantidad} unidad(es) - ${precio_producto} c/u - Subtotal: ${subtotal:.2f}\n"
                    total += subtotal

                # Mostrar la lista de productos y el total
                productos_str += f"\nTotal del pedido: ${total:.2f}"
                messagebox.showinfo("Productos Seleccionados", f"Productos en el pedido:\n{productos_str}")
            else:
                messagebox.showinfo("Sin Productos", "No se han agregado productos al pedido.")

        # Botón para ver los productos seleccionados
        boton_ver_productos = tk.Button(
            self.ventana_pedido_nuevo,
            text="Ver Productos Seleccionados",
            command=mostrar_productos_seleccionados,
            width=20,
            height=2
        )
        boton_ver_productos.pack(pady=20)

        # Botón para finalizar el pedido
        boton_finalizar_pedido = tk.Button(
            self.ventana_pedido_nuevo,
            text="Finalizar Pedido",
            command=self.finalizar_pedido,
            width=20,
            height=2
        )
        boton_finalizar_pedido.pack(pady=10)

        # Botón para volver atrás
        boton_volver = tk.Button(self.ventana_pedido_nuevo, text="Volver atrás", command=self.de_pedido_especifico_a_pedidos)
        boton_volver.pack()

    def de_pedido_especifico_a_pedidos(self):
        self.ventana_pedido_nuevo.withdraw()
        self.pedidos.deiconify()
        

    def finalizar_pedido(self):
        if not self.productos_seleccionados:
            messagebox.showwarning("Sin productos", "No has seleccionado ningún producto para el pedido.")
            return

        # Cargar los pedidos actuales del archivo JSON si existe
        pedidos_file = "pedidos.json"
        if os.path.exists(pedidos_file):
            with open(pedidos_file, 'r') as f:
                pedidos = json.load(f)
        else:
            pedidos = {}

        # Crear un nuevo pedido con un nombre incremental
        num_pedido = len(pedidos) + 1
        nombre_pedido = f"pedido{num_pedido}"

        # Preparar los datos del pedido
        productos_str = ""
        total = 0.0
        for nombre, cantidad in self.productos_seleccionados.items():
            producto = next(p for p in cargar_inventario() if p['nombre'] == nombre)
            precio_producto = producto['precio']
            subtotal = precio_producto * cantidad
            productos_str += f"{nombre} - {cantidad} unidad(es) - ${precio_producto} c/u - Subtotal: ${subtotal:.2f}\n"
            total += subtotal

        # Guardar los datos del pedido en el JSON
        pedidos[nombre_pedido] = {
            "productos": self.productos_seleccionados,
            "total": total
        }

        with open(pedidos_file, 'w') as f:
            json.dump(pedidos, f, indent=4)

        # Mostrar mensaje de éxito y limpiar la selección
        messagebox.showinfo("Pedido Finalizado", f"Tu pedido '{nombre_pedido}' ha sido realizado con éxito.")
        self.ventana_pedido_nuevo.destroy()  # Cierra la ventana del pedido









    def volver_panel_stock(self):
        self.pedidos.withdraw()
        self.ventana_stock.deiconify()
        
    def pedido_stock(self, info_especifica_stock):
        self.pedidos.withdraw()

        self.pedido_especifico_stock = tk.Toplevel(self.root)
        self.pedido_especifico_stock.title("Panel de Actor de Stock")
        self.pedido_especifico_stock.geometry("300x600")
        
        aplicar_fondo(self.pedido_especifico_stock)

        self.info_stock = tk.Label(self.pedido_especifico_stock, text=info_especifica_stock)
        self.info_stock.pack()

        volver = tk.Button(self.pedido_especifico_stock, text="Volver atrás", command=self.volver_pedidos_stock) 
        volver.pack()
    
    def volver_pedidos_stock(self):
        self.pedido_especifico_stock.withdraw()
        self.pedidos.deiconify()
    
    def volver_panel_stock_productos(self):
        self.ventana_agregar_producto.withdraw()
        self.ventana_stock.deiconify()

    def volver_login(self):
        self.ventana_dueño.destroy()
        self.mostrar_login()  # Vuelve a la ventana de login

    def crear_cuenta_empleado(self):
        self.ventana_dueño.destroy()
        ventana_crear = tk.Tk()
        ventana_crear.title("Crear Cuenta Empleado")
        ventana_crear.geometry("300x250")
        
        
        # Aplicar imagen de fondo
        aplicar_fondo(ventana_crear)
        
        tk.Label(ventana_crear, text="Nombre de usuario", font=("Arial", 12)).pack(pady=5)
        entrada_usuario = tk.Entry(ventana_crear, font=("Arial", 12))
        entrada_usuario.pack()

        tk.Label(ventana_crear, text="Contraseña", font=("Arial", 12)).pack(pady=5)
        entrada_contraseña = tk.Entry(ventana_crear, font=("Arial", 12))
        entrada_contraseña.pack()

        tk.Label(ventana_crear, text="Rol", font=("Arial", 12)).pack(pady=5)
        entrada_rol = tk.Entry(ventana_crear, font=("Arial", 12))
        entrada_rol.pack()

        def guardar():
            usuario = entrada_usuario.get()
            contraseña = entrada_contraseña.get()
            rol = entrada_rol.get()
            
            empleados = cargar_empleados()
            empleados[usuario] = {"contraseña": contraseña, "rol": rol, "sueldo": 0}
            guardar_empleados(empleados)
            
            messagebox.showinfo("Éxito", f"Empleado {usuario} creado con éxito.")
            ventana_crear.destroy()

        boton_guardar = tk.Button(ventana_crear, text="Guardar", command=guardar, bg="#4CAF50", fg="white", font=("Arial", 12), width=10)
        boton_guardar.pack(pady=10)

    def mostrar_empleados_para_modificar_sueldo(self):
        empleados = cargar_empleados()

        if not empleados:
            messagebox.showinfo("Sin empleados", "No hay empleados para modificar sueldo.")
            return

        self.ventana_dueño.destroy()  # Destruye la ventana principal.

        ventana_sueldo = tk.Tk()  # Nueva ventana para modificar sueldo.
        ventana_sueldo.title("Modificar Sueldo")
        ventana_sueldo.geometry("300x400")

        # Aplicar imagen de fondo
        aplicar_fondo(ventana_sueldo)

        tk.Label(ventana_sueldo, text="Selecciona un empleado", font=("Arial", 12)).pack(pady=10)

        # Crear botones por cada empleado
        for empleado in empleados:
            if empleado != "dueño":  # Omitir si es el dueño
                boton_empleado = tk.Button(
                    ventana_sueldo, 
                    text=empleado, 
                    command=lambda emp=empleado: self.modificar_sueldo(emp, ventana_sueldo), 
                    bg="#FFC107", fg="white", font=("Arial", 12), width=20
                )
                boton_empleado.pack(pady=5)

        boton_volver = tk.Button(ventana_sueldo, text="Volver Atrás", command=self.volver_dueño, bg="#F44336", fg="white", font=("Arial", 12), width=10)
        boton_volver.pack()

    def modificar_sueldo(self, empleado, ventana_anterior):
        ventana_anterior.destroy()  # Destruir la ventana anterior.

        ventana_sueldo = tk.Tk()  # Nueva ventana para modificar el sueldo.
        ventana_sueldo.title(f"Modificar Sueldo - {empleado}")
        ventana_sueldo.geometry("300x200")

        # Aplicar imagen de fondo
        aplicar_fondo(ventana_sueldo)

        tk.Label(ventana_sueldo, text=f"Nuevo sueldo para {empleado}", font=("Arial", 12)).pack(pady=5)
        entrada_sueldo = tk.Entry(ventana_sueldo, font=("Arial", 12))
        entrada_sueldo.pack(pady=10)
        
    

        # Función para guardar el nuevo sueldo
        def guardar_sueldo():
            nuevo_sueldo = entrada_sueldo.get()
            if not nuevo_sueldo.isdigit():
                messagebox.showerror("Error", "El sueldo debe ser un número válido.")
                return

            empleados = cargar_empleados()  # Cargar empleados desde el JSON.
            empleados[empleado]["sueldo"] = float(nuevo_sueldo)  # Actualizar sueldo.
            guardar_empleados(empleados)  # Guardar empleados actualizados en el JSON.

            messagebox.showinfo("Éxito", f"Sueldo de {empleado} actualizado.")
            ventana_sueldo.destroy()  # Cerrar la ventana de modificación.
        

        boton_guardar = tk.Button(ventana_sueldo, text="Guardar Sueldo", command=guardar_sueldo, bg="#4CAF50", fg="white", font=("Arial", 12), width=20)
        boton_guardar.pack(pady=10)
        
        def guardar_sueldo():
            nuevo_sueldo = entrada_sueldo.get()
            if not nuevo_sueldo.isdigit():
                messagebox.showerror("Error", "El sueldo debe ser un número válido.")
                return
            
            empleados = cargar_empleados()
            empleados[empleado]["sueldo"] = float(nuevo_sueldo)
            guardar_empleados(empleados)
            
            messagebox.showinfo("Éxito", f"Sueldo de {empleado} actualizado.")
            ventana_sueldo.destroy()

        boton_guardar = tk.Button(ventana_sueldo, text="Guardar Sueldo", command=guardar_sueldo, bg="#4CAF50", fg="white", font=("Arial", 12), width=20)
        boton_guardar.pack(pady=10)

    def mostrar_empleados_para_despedir(self):
        empleados = cargar_empleados()
        
        if not empleados:
            messagebox.showinfo("Sin empleados", "No hay empleados para despedir.")
            return
        
        self.ventana_dueño.destroy()  # Cierra la ventana del dueño
        
        self.ventana_despedir = tk.Toplevel(self.root)
        self.ventana_despedir.title("Despedir Empleado")
        self.ventana_despedir.geometry("300x400")
        
        aplicar_fondo(self.ventana_despedir)
        
        # Aplicar imagen de fondo
        aplicar_fondo(self.ventana_despedir)
        
        tk.Label(self.ventana_despedir, text="Selecciona un empleado", font=("Arial", 12)).pack(pady=10)
        
        # Crear botones con los nombres de los empleados
        for empleado in empleados:
            if empleado != "dueño":
                boton_empleado = tk.Button(self.ventana_despedir, text=empleado, command=lambda emp=empleado: self.despedir_empleado(emp), bg="#F44336", fg="white", font=("Arial", 12), width=20)
                boton_empleado.pack(pady=5)
        
        # Botón para volver atrás
        self.boton_volver = tk.Button(self.ventana_despedir, text="Volver Atrás", command=self.volver_dueño, bg="#F44336", fg="white", font=("Arial", 12), width=10)
        self.boton_volver.pack()

    def despedir_empleado(self, empleado):
        empleados = cargar_empleados()
        
        if empleado in empleados:
            del empleados[empleado]  # Eliminar al empleado del diccionario
            guardar_empleados(empleados)
            messagebox.showinfo("Éxito", f"Empleado {empleado} despedido.")
            self.ventana_despedir.destroy()
            self.mostrar_panel_dueño()  # Vuelve al panel del dueño

# Ejecución de la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()