from tkinter import *
from PIL import Image, ImageTk

# Components
from Controller.Controller import Controller

class ButtonView():
    def __init__(self, root, controller:Controller):
        self.root = root
        self.controller = controller
        
        #Botones
        self.image_button = Image.open("Sprites/Button/1.png")
        self.image_button = self.image_button.resize((100, 65), Image.ANTIALIAS) # Redimension (Alto, Ancho)
        self.image_button = ImageTk.PhotoImage(self.image_button)
    
    def cero(self):
        self.bton = Button(self.root,image=self.image_button, command = lambda: self.controller.function_button0())
        self.bton.place(x=623,y=330)
    
    def uno(self):
        self.bton = Button(self.root,image=self.image_button, command = lambda: self.controller.function_button1())
        self.bton.place(x=623,y=415)

    def dos(self):
        self.bton = Button(self.root,image=self.image_button, command = lambda: self.controller.function_button2())
        self.bton.place(x=20,y=330)

    def tres(self):
        self.bton = Button(self.root,image=self.image_button, command = lambda: self.controller.function_button3())
        self.bton.place(x=20,y=415)

    def cuatro(self):
        self.bton = Button(self.root,image=self.image_button, command = lambda: self.controller.function_button4())
        self.bton.place(x=623,y=250)

    def cinco(self):
        self.bton = Button(self.root, image=self.image_button, command = lambda: self.controller.function_button5())
        self.bton.place(x=20,y=250)