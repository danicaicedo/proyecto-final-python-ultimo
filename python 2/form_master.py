import tkinter as tk
from tkinter.font import BOLD
from customtkinter import CTk, CTkLabel, CTkButton
import util.generic as utl
from PIL import ImageTk, Image


class MasterPanel:
    def __init__(self):        
        self.ventana = tk.Tk()                             
        self.ventana.title('Master panel')
        w, h = self.ventana.winfo_screenwidth(), self.ventana.winfo_screenheight()                                    
        self.ventana.geometry("%dx%d+0+0" % (w, h))
        self.ventana.config(bg='#fcfcfc')
        self.ventana.resizable(width=0, height=0)            
        
        imagen = Image.open('imagenes/logo.jpg')
        imagen = ImageTk.PhotoImage(imagen)

        label = tk.Label(self.ventana, image=imagen, bg='#3a7ff6')
        label.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.ventana.mainloop()

# Crear una instancia de MasterPanel
master_panel = MasterPanel()
