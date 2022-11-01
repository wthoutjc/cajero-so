from tkinter import *
from tkinter import Frame, Canvas

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
        self.options = [BuilderPantalla0(), BuilderPantalla1(), BuilderPantalla2(), BuilderDavivienda()]
        self.app.set_builder(self.options[position])
        return self.app.build_cajero()

    def screen_welcome(self):
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

        self.label_name = Label(self.root,text= "Nombre").place(x=190, y=150)
        self.register_name = StringVar()
        self.txt_name = Entry(self.root,textvariable=self.register_name).place(x=250, y=150)
        self.label_id =Label(self.root,text= "Cédula").place(x=190, y=190)
        self.register_id = StringVar()
        self.txt_id = Entry(self.root, textvariable=self.register_id).place(x=250, y=190)
    
    def screen_login(self):
        self.controller.set_status(3)

        self.fondo = Label(self.root,image=self.set_screen(1), width = 445, height = 365 )
        self.fondo.place(x=150,y=125)
        self.text1 = Label(self.root, text = "Continuar" )
        self.text1.place(x=423, y = 455)
        self.text2 = Label(self.root, text = "Volver" )
        self.text2.place(x=423, y = 360)

        self.label_id =Label(self.root,text= "Cédula").place(x=190, y=150)
        self.login_id = StringVar()
        self.txt_id = Entry(self.root, textvariable=self.login_id).place(x=250, y=150)

    def screen_notification(self, message):
        self.controller.set_status(2)

        self.fondo = Label(self.root,image=self.set_screen(2), width = 445, height = 365 )
        self.fondo.place(x=150,y=125)

        self.message = Label(self.root, text = message)
        self.message.place(x=223, y = 160)

        self.text1 = Label(self.root, text = "Volver")
        self.text1.place(x=423, y = 455)

    def screen_davivienda(self, name, id, transacciones, turno):
        self.controller.set_status(4)

        self.fondo = Label(self.root,image=self.set_screen(3), width = 445, height = 365 )
        self.fondo.place(x=150,y=125)

        self.text1 = Label(self.root, text = "Atender mis transacciones")
        self.text1.place(x=373, y = 455)
        self.text2 = Label(self.root, text = "Añadir transacción")
        self.text2.place(x=403, y = 360)
        self.text3 = Label(self.root, text = "Salir")
        self.text3.place(x=233, y = 455)

        self.text3 = Label(self.root, text = "Nombre: " + name)
        self.text3.place(x=163, y = 140)
        self.text4 = Label(self.root, text = "Cédula: " + id)
        self.text4.place(x=163, y = 170)
        self.text5 = Label(self.root, text = "Transacciones: " + str(transacciones))
        self.text5.place(x=163, y = 200)
        self.text6 = Label(self.root, text = "Turno: " + str(turno))
        self.text6.place(x=163, y = 230)

    def get_register_name(self):
        return self.register_name.get()

    def get_register_id(self):
        return self.register_id.get()

    def get_login_id(self):
        return self.login_id.get()

    def get_root(self):
        return self.root