from abc import ABC, abstractmethod

from View.FactoriaInterfaz import *

class AbstractBuilder(ABC):
    @abstractmethod
    def __init__(self):
        self.abstract_interfaz = None
    
    @abstractmethod
    def build_pantalla(self):
        pass

class BuilderPantalla0(AbstractBuilder):
    def __init__(self):
        self.abstract_interfaz = FabricaScreenPrincipal()
    
    def build_pantalla(self):
        return self.abstract_interfaz.crear_pantalla()

class BuilderPantalla1(AbstractBuilder):
    def __init__(self):
        self.abstract_interfaz = FabricaScreens()
    
    def build_pantalla(self):
        return self.abstract_interfaz.crear_pantalla()

class BuilderPantalla2(AbstractBuilder):
    def __init__(self):
        self.abstract_interfaz = FabricaScreens2()
    
    def build_pantalla(self):
        return self.abstract_interfaz.crear_pantalla()

class BuilderAgrario(AbstractBuilder):
    def __init__(self):
        self.abstract_interfaz = FabricaAgrario()
    
    def build_pantalla(self):
        return self.abstract_interfaz.crear_pantalla()

class BuilderBancolombia(AbstractBuilder):
    def __init__(self):
        self.abstract_interfaz = FabricaBancolombia()
    
    def build_pantalla(self):
        return self.abstract_interfaz.crear_pantalla()

class BuilderDavivienda(AbstractBuilder):
    def __init__(self):
        self.abstract_interfaz = FabricaDavivienda()
    
    def build_pantalla(self):
        return self.abstract_interfaz.crear_pantalla()

class BuilderManager():
    def __init__(self):
        self.builder = None
    
    def set_builder(self, builder: AbstractBuilder):
        self.builder = builder
    
    def build_cajero(self):
        return self.builder.build_pantalla()