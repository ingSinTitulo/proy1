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

    def avanzar(self, pasos=1):
        self.posicion += pasos
        self.columna += pasos
        if self.posicion > len(self.texto) - 1:
            self.caracterActual = None
        else:
            self.caracterAnterior = self.texto[self.posicion-1]
            self.caracterActual = self.texto[self.posicion]

    def simbolosIgnorados(self):
        while self.caracterActual is not None and self.caracterActual.isspace():
            self.avanzar()

    def palabra(self):
        palabras = ""
        if self.caracterAnterior in ['"', "'"]:
            final = self.caracterAnterior
            while self.caracterActual is not None and self.caracterActual != final:
                palabras += self.caracterActual
                self.avanzar()
            return diccionarios.SIMBOLIZAR("ATTR_VALUE", palabras)
        elif self.caracterAnterior == ">":
            while self.caracterActual is not None and self.caracterActual != '<':
                palabras += self.caracterActual
                self.avanzar()
            return diccionarios.SIMBOLIZAR("HTML_INNERTEXT", palabras)
        else:
            while self.caracterActual is not None and (self.caracterActual.isalnum() or self.caracterActual in ["-", "."]):
                palabras += self.caracterActual
                self.avanzar()
            return diccionarios.etiquetas.get(palabras, diccionarios.SIMBOLIZAR("ATTR_NAME", palabras))

    def excepcion(self):
        raise Exception("Caracter no reconocido: " + self.caracterActual)

    def cargarSiguienteSimbolo(self):
        while self.caracterActual is not None:
            if self.caracterActual.isspace():
                if self.caracterActual == "\n":
                    self.linea += 1
                    self.columna = 1
                self.simbolosIgnorados()
                continue
            elif self.caracterAnterior in ["'", '"'] and self.texto[self.posicion-2]=="=":
                return self.palabra()
            elif self.caracterActual.isalpha():
                return self.palabra()
            elif self.caracterActual in list(diccionarios.simbolos.keys()):
                temp = self.caracterActual
                self.avanzar()
                return diccionarios.simbolos.get(temp)
            elif self.caracterActual == "!" and self.caracterAnterior == "<":
                while self.caracterActual is not None and self.caracterActual != ">":
                    self.avanzar()
                return diccionarios.SIMBOLIZAR("COMMENT", "comentario")
            elif self.caracterAnterior == ">":
                return self.palabra()
            else:
                self.excepcion()
        return diccionarios.SIMBOLIZAR("FIN", None)