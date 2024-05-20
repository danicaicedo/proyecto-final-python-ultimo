import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
from tkinter import ttk
import csv

from form_master import MasterPanel

class App:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title('Afiliar Socio')
        self.ventana.geometry('800x500')
        self.ventana.config(bg='#fcfcfc')
        self.ventana.resizable(width=0, height=0)

        # Leer y redimensionar la imagen
        imagen = Image.open('imagenes/logo.jpg')
        imagen = imagen.resize((200, 200), Image.BILINEAR)
        imagen = ImageTk.PhotoImage(imagen)

        # Crear el marco para el logotipo
        frame_logo = tk.Frame(self.ventana, bd=0, width=300,
                              relief=tk.SOLID, padx=20, pady=150, bg='#000000')
        frame_logo.pack(side="left", expand=tk.NO, fill=tk.NONE)
        label = tk.Label(frame_logo, image=imagen, bg='#000000')
        label.pack()

        # Crear un marco vacío para el espacio en blanco
        frame_blank = tk.Frame(self.ventana, bg='#fcfcfc')
        frame_blank.pack(side="left", expand=tk.YES, fill=tk.BOTH)

        # Crear el marco superior para el formulario
        frame_form = tk.Frame(self.ventana, height=50, bd=0, relief=tk.SOLID, bg='black')
        frame_form.pack(side="top", fill=tk.X, padx=150)  

        title = tk.Label(frame_form, text="Afiliar Socio", font=(
            'Times', 30), fg="#666a88", bg='#fcfcfc', pady=1)
        title.pack(expand=tk.YES, fill=tk.BOTH)

        # frame_form_fill
        frame_form_fill = tk.Frame(
            frame_form, height=50,  bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form_fill.pack(side="bottom", expand=tk.YES, fill=tk.BOTH)

        etiqueta_nombre = tk.Label(frame_form_fill, text="Nombre del socio", font=(
            'Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
        etiqueta_nombre.pack(fill=tk.X, padx=20, pady=5)
        self.nombre_socio = ttk.Entry(frame_form_fill, font=('Times', 14))
        self.nombre_socio.insert(0, "")
        self.nombre_socio.pack(fill=tk.X, padx=20, pady=10)

        etiqueta_cedula = tk.Label(frame_form_fill, text="Cédula", font=(
            'Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
        etiqueta_cedula.pack(fill=tk.X, padx=20, pady=5)
        self.cedula_socio = ttk.Entry(frame_form_fill, font=('Times', 14))
        self.cedula_socio.insert(0, "")
        self.cedula_socio.pack(fill=tk.X, padx=20, pady=10)

        etiqueta_password = tk.Label(frame_form_fill, text="Contraseña", font=(
            'Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
        etiqueta_password.pack(fill=tk.X, padx=20, pady=5)
        self.password = ttk.Entry(frame_form_fill, font=('Times', 14))
        self.password.pack(fill=tk.X, padx=20, pady=10)
        self.password.config(show="*")

        inicio = tk.Button(frame_form_fill, text="Afiliar Socio", font=(
            'Times', 15), bg='#3a7ff6', bd=0, fg="#fff", command=self.verificar)
        inicio.pack(fill=tk.X, padx=20, pady=20)
        inicio.bind("<Return>", (lambda event: self.verificar()))

        # Cargar las cédulas registradas desde el archivo CSV
        self.cedulas_registradas = self.cargar_cedulas_registradas()

        self.ventana.mainloop()

    def verificar(self):
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

        # Guardar las cédulas registradas en el archivo CSV
        self.guardar_cedulas_registradas()

        messagebox.showinfo(message="Socio afiliado con éxito.", title="Éxito")

        self.nombre_socio.delete(0, tk.END)
        self.cedula_socio.delete(0, tk.END)
        self.password.delete(0, tk.END)

        self.ventana.destroy()
        master_panel = MasterPanel()

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

App_ = App()
