class AbstractProducto():
    def __init__(self):
        self.image=''

    def get_image(self):
        return self.image

class Pantalla0(AbstractProducto):
    def __init__(self):
        self.image = 'Sprites/Pantalla/1.png'
        
class Pantalla1(AbstractProducto):
    def __init__(self):
        self.image = 'Sprites/Pantalla/1.png'

class Pantalla2(AbstractProducto):
    def __init__(self):
        self.image = 'Sprites/Pantalla/2.png'

class PantallaAgrario(AbstractProducto):
    def __init__(self):
        self.image = 'Sprites/Pantalla/Agrario.png'

class PantallaBancolombia(AbstractProducto):
    def __init__(self):
        self.image = 'Sprites/Pantalla/Bancolombia.png'

class PantallaDavivienda(AbstractProducto):
    def __init__(self):
        self.image = 'Sprites/Pantalla/Davivienda.png'