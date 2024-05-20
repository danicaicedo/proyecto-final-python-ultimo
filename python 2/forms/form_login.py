import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
from tkinter import ttk
import csv

class App:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title('Afiliar Socio')
        self.ventana.geometry('800x500')
        self.ventana.config(bg='#fcfcfc')
        self.ventana.resizable(width=0, height=0)
        self.socios_registrados = []

        # Leer y redimensionar la imagen
        imagen = Image.open('imagenes/logo.jpg')
        imagen = imagen.resize((200, 200), Image.BILINEAR)
        imagen = ImageTk.PhotoImage(imagen)

        # Crear el marco para el logotipo
        frame_logo = tk.Frame(self.ventana, bd=0, width=300, relief=tk.SOLID, padx=20, pady=150, bg='#000000')
        frame_logo.pack(side="left", expand=tk.NO, fill=tk.NONE)
        label = tk.Label(frame_logo, image=imagen, bg='#000000')
        label.pack()

        # Crear un marco vacío para el espacio en blanco
        frame_blank = tk.Frame(self.ventana, bg='#fcfcfc')
        frame_blank.pack(side="left", expand=tk.YES, fill=tk.BOTH)

        # Crear el marco superior para el formulario
        frame_form = tk.Frame(self.ventana, height=50, bd=0, relief=tk.SOLID, bg='black')
        frame_form.pack(side="top", fill=tk.X, padx=150)  

        title = tk.Label(frame_form, text="Afiliar Socio", font=('Times', 22), fg="#666a88", bg='#fcfcfc', pady=1)
        title.pack(expand=tk.YES, fill=tk.BOTH)

        # frame_form_fill
        frame_form_fill = tk.Frame(frame_form, height=50, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form_fill.pack(side="bottom", expand=tk.YES, fill=tk.BOTH)

        etiqueta_nombre = tk.Label(frame_form_fill, text="Nombre del socio", font=('Times', 12), fg="#666a88", bg='#fcfcfc', anchor="w")
        etiqueta_nombre.pack(fill=tk.X, padx=20, pady=5)
        self.nombre_socio = ttk.Entry(frame_form_fill, font=('Times', 12))
        self.nombre_socio.insert(0, "")
        self.nombre_socio.pack(fill=tk.X, padx=20, pady=10)

        etiqueta_cedula = tk.Label(frame_form_fill, text="Cédula", font=('Times', 12), fg="#666a88", bg='#fcfcfc', anchor="w")
        etiqueta_cedula.pack(fill=tk.X, padx=20, pady=5)
        self.cedula_socio = ttk.Entry(frame_form_fill, font=('Times', 12))
        self.cedula_socio.insert(0, "")
        self.cedula_socio.pack(fill=tk.X, padx=20, pady=10)

        etiqueta_password = tk.Label(frame_form_fill, text="Contraseña", font=('Times', 12), fg="#666a88", bg='#fcfcfc', anchor="w")
        etiqueta_password.pack(fill=tk.X, padx=20, pady=5)
        self.password = ttk.Entry(frame_form_fill, font=('Times', 12))
        self.password.pack(fill=tk.X, padx=20, pady=10)
        self.password.config(show="*")

        etiqueta_tipo_socio = tk.Label(frame_form_fill, text="Seleccione tipo de socio:", font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
        etiqueta_tipo_socio.pack(fill=tk.X, padx=20, pady=5)
        self.tipo_socio = ttk.Combobox(frame_form_fill, values=["VIP", "No VIP"], font=('Times', 14))
        self.tipo_socio.pack(fill=tk.X, padx=20, pady=10)


        # Botón Afiliar Socio
        btn_afiliar = tk.Button(frame_form_fill, text="Afiliar Socio", font=('Times', 10), bg='#3a7ff6', bd=0, fg="#fff", command=self.afiliar_socio)
        btn_afiliar.pack(fill=tk.X, padx=10, pady=10)
        btn_afiliar.bind("<Return>", (lambda event: self.afiliar_socio()))

        # Botón Entrar
        btn_entrar = tk.Button(frame_form_fill, text="Entrar", font=('Times', 10), bg='#3a7ff6', bd=0, fg="#fff", command=self.entrar)
        btn_entrar.pack(fill=tk.X, padx=10, pady=10)
        btn_entrar.bind("<Return>", (lambda event: self.entrar()))
        
        # Botón Persona Referida
        btn_referido = tk.Button(frame_form_fill, text="Persona Referida", font=('Times', 10), bg='#3a7ff6', bd=0, fg="#fff", command=self.registrar_referido)
        btn_referido.pack(fill=tk.X, padx=10, pady=10)
        btn_referido.bind("<Return>", (lambda event: self.registrar_referido()))

        # Cargar las cédulas registradas desde el archivo CSV
        self.cedulas_registradas = self.cargar_cedulas_registradas()
        self.autorizados_registrados = self.cargar_autorizados_registrados()

        # Cargar los socios registrados desde el archivo CSV
        self.socios_registrados = self.cargar_socios_registrados()

        self.ventana.mainloop()

    def afiliar_socio(self):
        nombre = self.nombre_socio.get()
        cedula = self.cedula_socio.get()
        password = self.password.get()
        tipo_socio = self.tipo_socio.get()

        if nombre == "" or cedula == "" or password == "" or tipo_socio == "":
           messagebox.showerror(message="Por favor, complete todos los campos.", title="Error")
           return

    # Verificar si la cédula ya está registrada
        if cedula in self.cedulas_registradas:
            messagebox.showerror(message="La cédula ingresada ya está registrada.", title="Error")
            return

    # Si la cédula no está registrada, continuar con la afiliación del socio
        nuevo_socio = {
             "nombre": nombre,
              "cedula": cedula,
              "password": password,
              "fondos": 0,
               "VIP": tipo_socio,
               "facturas": 0  # Suponiendo que las facturas iniciales son 0
    }

    # Agregar la cédula del nuevo socio al conjunto de cédulas registradas
        self.cedulas_registradas.add(cedula)
        self.socios_registrados.append(nuevo_socio)  # Añadir el nuevo socio a la lista de socios registrados

    # Guardar las cédulas registradas en el archivo CSV
        self.guardar_cedulas_registradas()

        messagebox.showinfo(message="Socio afiliado con éxito.", title="Éxito")

        self.nombre_socio.delete(0, tk.END)
        self.cedula_socio.delete(0, tk.END)
        self.password.delete(0, tk.END)
        self.tipo_socio.set('')

        

    def entrar(self):
        # Obtener los datos ingresados por el usuario
        cedula = self.cedula_socio.get().lower()  # Convertir a minúsculas
        password = self.password.get().lower()    # Convertir a minúsculas

        # Verificar si se ingresaron todos los campos
        if cedula == "" or password == "":
            messagebox.showerror(message="Por favor, complete todos los campos.", title="Error")
            return

        # Verificar si la cédula y la contraseña coinciden con un socio registrado
        socio_encontrado = None
        for socio in self.socios_registrados:
            if socio["cedula"].lower() == cedula and socio["password"].lower() == password:
                socio_encontrado = socio
                break

        # Si se encuentra un socio con las credenciales proporcionadas, mostrar información del socio
        if socio_encontrado:
        # Crear una nueva ventana para mostrar la información del socio
            ventana_socio = tk.Toplevel()
            ventana_socio.title("Información del Socio")
            ventana_socio.geometry('400x300')
            ventana_socio.config(bg='#fcfcfc')
            ventana_socio.resizable(width=0, height=0)

        # Mostrar la información del socio en la nueva ventana
            

            etiqueta_nombre = tk.Label(ventana_socio, text=f"Nombre: {socio_encontrado['nombre']}", font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
            etiqueta_nombre.pack(fill=tk.X, padx=20, pady=5)
            
            etiqueta_cedula = tk.Label(ventana_socio, text=f"Cédula: {socio_encontrado['cedula']}", font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
            etiqueta_cedula.pack(fill=tk.X, padx=20, pady=5)

            etiqueta_fondos = tk.Label(ventana_socio, text=f"Fondos Disponibles: {socio_encontrado['fondos']}", font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
            etiqueta_fondos.pack(fill=tk.X, padx=20, pady=5)

            etiqueta_vip = tk.Label(ventana_socio, text=f"Tipo de Socio: {socio_encontrado['VIP']}", font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
            etiqueta_vip.pack(fill=tk.X, padx=20, pady=5)

            etiqueta_facturas = tk.Label(ventana_socio, text=f"Facturas Pendientes: {socio_encontrado['facturas']}", font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
            etiqueta_facturas.pack(fill=tk.X, padx=20, pady=5)

        else:
            messagebox.showerror(message="Cédula o contraseña incorrecta. Por favor, inténtelo de nuevo.", title="Error")

    def registrar_referido(self):
        # Aquí va la acción para el botón "Persona Referida"
        nombre = self.nombre_socio.get()
        cedula = self.cedula_socio.get()
        password = self.password.get()

        if nombre == "" or cedula == "" or password == "":
            messagebox.showerror(message="Por favor, complete todos los campos.", title="Error")
            return

        # Verificar si la cédula ya está registrada
        if cedula in self.cedulas_registradas:
            messagebox.showerror(message="La cédula ingresada ya está registrada.", title="Error")
            return

        # Si la cédula no está registrada, continuar con la afiliación del socio
        nuevo_socio = {
            "nombre": nombre,
            "cedula": cedula,
            "password": password,
            "fondos": 0
            # Puedes agregar más detalles del socio aquí si es necesario
        }

        # Agregar la cédula del nuevo socio al conjunto de cédulas registradas
        self.cedulas_registradas.add(cedula)

        # Agregar el nuevo socio a la lista de socios registrados
        self.socios_registrados.append(nuevo_socio)

        # Guardar las cédulas registradas y los socios registrados en los archivos CSV
        self.guardar_cedulas_registradas()
        self.guardar_socios_registrados()

        messagebox.showinfo(message="Socio afiliado con éxito.", title="Éxito")

        self.nombre_socio.delete(0, tk.END)
        self.cedula_socio.delete(0, tk.END)
        self.password.delete(0, tk.END)

        # Abrir ventana para registrar autorizado
        self.abrir_ventana_registrar_autorizado(cedula)

    def abrir_ventana_registrar_autorizado(self, cedula_socio):
        ventana_autorizado = tk.Toplevel()
        ventana_autorizado.title("Registrar Persona Autorizada")
        ventana_autorizado.geometry('400x300')
        ventana_autorizado.config(bg='#fcfcfc')
        ventana_autorizado.resizable(width=0, height=0)

        etiqueta_nombre = tk.Label(ventana_autorizado, text="Nombre del autorizado", font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
        etiqueta_nombre.pack(fill=tk.X)

        nombre_autorizado = ttk.Entry(ventana_autorizado, font=('Times', 14))
        nombre_autorizado.pack(fill=tk.X, padx=20, pady=10)

        etiqueta_cedula = tk.Label(ventana_autorizado, text="Cédula del autorizado", font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
        etiqueta_cedula.pack(fill=tk.X, padx=20, pady=5)
        cedula_autorizado = ttk.Entry(ventana_autorizado, font=('Times', 14))
        cedula_autorizado.pack(fill=tk.X, padx=20, pady=10)

        registrar_btn = tk.Button(ventana_autorizado, text="Registrar Autorizado", font=('Times', 15), bg='#3a7ff6', bd=0, fg="#fff", 
                                  command=lambda: self.registrar_autorizado(cedula_socio, nombre_autorizado.get(), cedula_autorizado.get(), ventana_autorizado))

        registrar_btn.pack(fill=tk.X, padx=20, pady=20)

    def registrar_autorizado(self, cedula_socio, nombre_autorizado, cedula_autorizado, ventana_autorizado):
        if nombre_autorizado == "" or cedula_autorizado == "":
            messagebox.showerror(message="Por favor, complete todos los campos.", title="Error")
            return

        if cedula_autorizado in [autorizado["cedula_autorizado"] for autorizado in self.autorizados_registrados]:
            messagebox.showerror(message="La cédula del autorizado ya está registrada.", title="Error")
            return

        nuevo_autorizado = {
            "cedula_socio": cedula_socio,
            "nombre_autorizado": nombre_autorizado,
            "cedula_autorizado": cedula_autorizado
        }

        self.autorizados_registrados.append(nuevo_autorizado)
        self.guardar_autorizados_registrados()

        messagebox.showinfo(message="Persona autorizada registrada con éxito.", title="Éxito")
        ventana_autorizado.destroy()

    def cargar_cedulas_registradas(self):
        try:
            with open('cedulas_registradas.csv', 'r') as file:
                reader = csv.reader(file)
                cedulas = set()
                for row in reader:
                    cedulas.add(row[0])
                return cedulas
        except FileNotFoundError:
            return set()

    def guardar_cedulas_registradas(self):
        with open('cedulas_registradas.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for cedula in self.cedulas_registradas:
                writer.writerow([cedula])

    def cargar_socios_registrados(self):
        try:
             with open('socios_registrados.csv', 'r') as file:
                 reader = csv.DictReader(file)
                 socios = []
                 for row in reader:
                     socios.append({
                    "nombre": row["nombre"],
                    "cedula": row["cedula"],
                    "password": row["password"],
                    "fondos": int(row["fondos"]),
                    "VIP": row["VIP"],
                    "facturas": int(row["facturas"])
                })
                 return socios
        except FileNotFoundError:
            return []


    def guardar_socios_registrados(self):
        with open('socios_registrados.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for socio in self.socios_registrados:
                writer.writerow([socio["nombre"], socio["cedula"], socio["password"], socio["fondos"]])

    def cargar_autorizados_registrados(self):
        try:
            with open('autorizados_registrados.csv', 'r') as file:
                reader = csv.reader(file)
                autorizados = []
                for row in reader:
                    autorizados.append({
                        "cedula_socio": row[0],
                        "nombre_autorizado": row[1],
                        "cedula_autorizado": row[2]
                    })
                return autorizados
        except FileNotFoundError:
            return []

    def guardar_autorizados_registrados(self):
        with open('autorizados_registrados.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for autorizado in self.autorizados_registrados:
                writer.writerow([autorizado["cedula_socio"], autorizado["nombre_autorizado"], autorizado["cedula_autorizado"]])

App_ = App()
