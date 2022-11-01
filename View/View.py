from tkinter import *
from tkinter import Frame, Canvas
from tkinter import ttk

from PIL import Image, ImageTk

# Components
from Controller.Controller import Controller
from View.Button import ButtonView
from View.Builder import *

class View():
    def __init__(self, title, controller:Controller):
        self.controller = controller

        # Conf. ventana
        self.root = Tk()
        self.root.title(title)
        self.root.geometry("749x721")
        self.root.resizable(width=0, height=0)

        # Imagen - fondo
        self.ifo = Image.open("Sprites/Cajero/DiseñoSprites.png")
        self.ifo.thumbnail((749,721))
        self.ifo = ImageTk.PhotoImage(self.ifo)
        self.image_principal = Label(self.root, image=self.ifo, width = 1000, height = 980)
        self.image_principal.pack()

        #Buttons
        self.button = ButtonView(self.root, self.controller)
        self.button.cero()
        self.button.uno()
        self.button.dos()
        self.button.tres()
        self.button.cuatro()
        self.button.cinco()
    
    def set_screen(self, position: int):
        self.sub_interfaz = Image.open(self.get_builder(position))
        self.sub_interfaz.thumbnail((465,365))
        self.sub_interfaz = ImageTk.PhotoImage(self.sub_interfaz)
        return self.sub_interfaz
    
    def get_builder(self, position: int):
        self.app = BuilderManager()
        self.options = [BuilderPantalla0(), BuilderPantalla1(), BuilderPantalla2(), BuilderAgrario(), BuilderBancolombia(), BuilderDavivienda()]
        self.app.set_builder(self.options[position])
        return self.app.build_cajero()

    def screen_login(self):
        self.controller.set_status(0)

        self.fondo = Label(self.root,image=self.set_screen(0), width = 445, height = 365 )
        self.fondo.place(x=150,y=125)
        self.text1 = Label(self.root, text = "Registrarse" )
        self.text1.place(x=423, y = 455)
        self.text2 = Label(self.root, text = "Iniciar sesión" )
        self.text2.place(x=423, y = 360)

    def screen_register(self):
        self.controller.set_status(1)

        self.fondo = Label(self.root,image=self.set_screen(1), width = 445, height = 365 )
        self.fondo.place(x=150,y=125)
        self.text1 = Label(self.root, text = "Continuar" )
        self.text1.place(x=423, y = 455)
        self.text2 = Label(self.root, text = "Volver" )
        self.text2.place(x=423, y = 360)

        self.lblName = Label(self.root,text= "Nombre").place(x=190, y=150)
        self.nombreUsu = StringVar()
        self.txtName = Entry(self.root,textvariable=self.nombreUsu).place(x=250, y=150)
        self.lblApellido =Label(self.root,text= "Apellido").place(x=190, y=190)
        self.apellidoUsu = StringVar()
        self.txtApellido = Entry(self.root,textvariable=self.apellidoUsu).place(x=250, y=190)
        self.lblIdPersona =Label(self.root,text="Cedula").place(x=190, y=230)
        self.idPersona = StringVar()
        self.txtIdPersona = Entry(self.root,textvariable=self.idPersona).place(x=250, y=230)
        self.lblBanco =Label(self.root,text= "Banco").place(x=390, y=150)
        self.comboboxbanco = ttk.Combobox(self.root, state = "readonly" )
        self.comboboxbanco.place(x=440, y=150)
        self.comboboxbanco["values"] = ["Agrario", "Bancolombia", "Davivienda"]
        self.lblSaldo =Label(self.root,text= "Saldo Inicial").place(x=175, y=270)
        self.saldo = StringVar()
        self.txtsaldo = Entry(self.root,textvariable=self.saldo).place(x=250, y=270)
        self.lblPassword =Label(self.root,text= "Password").place(x=190, y=300)
        self.password = StringVar()
        self.txtclave = Entry(self.root,textvariable=self.password).place(x=250, y=300)

    def get_root(self):
        return self.root