from abc import ABC, abstractmethod

from View.ProductoInterfaz import *

class AbstractInterfaz(ABC):
    @abstractmethod
    def crear_pantalla(self):
        pass

class FabricaScreenPrincipal(AbstractInterfaz):
    def crear_pantalla(self):
        return Pantalla0().get_image()

class FabricaScreens(AbstractInterfaz):
    def crear_pantalla(self):
        return Pantalla1().get_image()

class FabricaScreens2(AbstractInterfaz):
    def crear_pantalla(self):
        return Pantalla2().get_image()

class FabricaDavivienda(AbstractInterfaz):
    def crear_pantalla(self):
        return PantallaDavivienda().get_image()