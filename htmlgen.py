"""
HTMLGEN: Generador de HTML5 mediante JavaScript ES5.
Copyright 2019 Jesus Alan Ramirez Zatarain.
"""
import diccionarios

class HTMLGEN:
    def __init__(self, texto):
        self.texto = texto
        self.posicion = 0
        self.caracterActual = self.texto[self.posicion]
        self.caracterAnterior = None
        self.columna = 0
        self.linea = 1

    def cargarSiguienteSimbolo(self):
        while self.caracterActual is not None:
            if self.caracterActual.isspace():
                if self.caracterActual == "\n":
                    self.linea += 1
                while self.caracterActual is not None and self.caracterActual.isspace():
                    self.posicion += 1
                    self.columna += 1
                    if self.posicion > len(self.texto) - 1:
                        self.caracterActual = None
                    else:
                        self.caracterAnterior = self.texto[self.posicion-1]
                        self.caracterActual = self.texto[self.posicion]
                self.columna = 1
                continue
            elif self.caracterActual.isalpha():
                cadenaEncontrada = ""
                while self.caracterActual is not None and self.caracterActual.isalnum():
                    cadenaEncontrada += self.caracterActual
                    self.posicion += 1
                    self.columna += 1
                    if self.posicion > len(self.texto) - 1:
                        self.caracterActual = None
                    else:
                        self.caracterActual = self.texto[self.posicion]
                        self.caracterAnterior = self.texto[self.posicion-1]
                return diccionarios.etiquetas.get(cadenaEncontrada)
            raise Exception("Caracter no reconocido: " + self.caracterActual)
        return SIMBOLIZAR("FIN", None)