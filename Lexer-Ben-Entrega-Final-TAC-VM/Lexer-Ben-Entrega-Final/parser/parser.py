
"""Analizador sintactico que construye el AST."""
from typing import List

from lexer.token import Token
from arbol_ast.nodos import (
    NodoAST,
    Programa,
    Declaracion,
    Asignacion,
    Numero,
    DecimalLiteral,
    Cadena,
    Booleano,
    Identificador,
    OpBinaria,
    OpUnaria,
    Imprimir,
    Si,
    Mientras,
)


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.posicion = 0

        if not tokens or tokens[-1].tipo != "EOF":
            raise ValueError("La lista de tokens debe terminar con EOF.")

    @property
    def actual(self):
        return self.tokens[self.posicion]

    def avanzar(self):
        token = self.actual

        if token.tipo != "EOF":
            self.posicion += 1

        return token

    def es(self, esperado):
        return (
            self.actual.tipo == esperado
            or self.actual.valor == esperado
        )

    def coincidir(self, esperado):
        if self.es(esperado):
            return self.avanzar()

        raise SyntaxError(
            f"[Error Sintactico] Se esperaba '{esperado}', "
            f"pero se encontro '{self.actual.valor}' "
            f"en linea {self.actual.linea}."
        )

    def parsear(self):
        sentencias = []

        while self.actual.tipo != "EOF":
            sentencias.append(self.sentencia())

        return Programa(sentencias)

    # ---------------- SENTENCIAS ----------------

    def sentencia(self):
        if self.es("PR_ENTERO") or self.es("PR_DECIMAL"):
            return self.declaracion()

        if self.es("ID"):
            return self.asignacion()

        if self.es("PR_IMPRIMIR"):
            return self.sentencia_imprimir()

        if self.es("PR_SI"):
            return self.sentencia_si()

        if self.es("PR_MIENTRAS"):
            return self.sentencia_mientras()

        raise SyntaxError(
            f"[Error Sintactico] Sentencia no reconocida: "
            f"'{self.actual.valor}' en linea {self.actual.linea}."
        )

    def declaracion(self):
        tipo_token = self.avanzar()
        tipo = tipo_token.valor

        identificador = self.coincidir("ID")
        self.coincidir("ASIGNACION")
        expr = self.expresion()
        self.coincidir(";")

        return Declaracion(
            tipo,
            identificador.valor,
            expr,
            tipo_token.linea
        )

    def asignacion(self):
        identificador = self.coincidir("ID")
        self.coincidir("ASIGNACION")
        expr = self.expresion()
        self.coincidir(";")

        return Asignacion(
            identificador.valor,
            expr,
            identificador.linea
        )

    def sentencia_imprimir(self):
        self.coincidir("PR_IMPRIMIR")
        self.coincidir("(")
        expr = self.expresion()
        self.coincidir(")")
        self.coincidir(";")

        return Imprimir(expr)

    def sentencia_si(self):
        self.coincidir("PR_SI")
        self.coincidir("(")
        condicion = self.expresion()
        self.coincidir(")")
        bloque = self.bloque()

        return Si(condicion, bloque)

    def sentencia_mientras(self):
        self.coincidir("PR_MIENTRAS")
        self.coincidir("(")
        condicion = self.expresion()
        self.coincidir(")")
        bloque = self.bloque()

        return Mientras(condicion, bloque)

    def bloque(self):
        self.coincidir("{")
        sentencias = []

        while not self.es("}") and self.actual.tipo != "EOF":
            sentencias.append(self.sentencia())

        if self.actual.tipo == "EOF":
            raise SyntaxError(
                f"[Error Sintactico] Falta cerrar el bloque con '}}' "
                f"en linea {self.actual.linea}."
            )

        self.coincidir("}")
        return sentencias

    # ---------------- EXPRESIONES ----------------

    # OR: ||
    def expresion(self):
        return self.logico_or()

    def logico_or(self):
        nodo = self.logico_and()

        while self.es("OP_LOGICO") and self.actual.valor == "||":
            operador = self.avanzar()
            derecho = self.logico_and()
            nodo = OpBinaria(nodo, operador.valor, derecho)

        return nodo

    # AND: &&
    def logico_and(self):
        nodo = self.relacional()

        while self.es("OP_LOGICO") and self.actual.valor == "&&":
            operador = self.avanzar()
            derecho = self.relacional()
            nodo = OpBinaria(nodo, operador.valor, derecho)

        return nodo

    # Comparaciones: ==, !=, <, >, <=, >=
    def relacional(self):
        nodo = self.aritmetica()

        while self.es("OP_REL"):
            operador = self.avanzar()
            derecho = self.aritmetica()
            nodo = OpBinaria(nodo, operador.valor, derecho)

        return nodo

    # Suma y resta
    def aritmetica(self):
        nodo = self.termino()

        while self.es("OP_ARIT") and self.actual.valor in ("+", "-"):
            operador = self.avanzar()
            derecho = self.termino()
            nodo = OpBinaria(nodo, operador.valor, derecho)

        return nodo

    # Multiplicacion y division
    def termino(self):
        nodo = self.factor()

        while self.es("OP_ARIT") and self.actual.valor in ("*", "/"):
            operador = self.avanzar()
            derecho = self.factor()
            nodo = OpBinaria(nodo, operador.valor, derecho)

        return nodo

    # Valores, identificadores y expresiones agrupadas
    def factor(self):
        token = self.actual

        if self.es("OP_LOGICO") and token.valor == "!":
            self.avanzar()
            return OpUnaria("!", self.factor())

        if self.es("OP_ARIT") and token.valor in ("+", "-"):
            self.avanzar()
            return OpUnaria(token.valor, self.factor())

        if self.es("NUMERO"):
            self.avanzar()
            return Numero(int(token.valor))

        if self.es("DECIMAL"):
            self.avanzar()
            return DecimalLiteral(float(token.valor))

        if self.es("CADENA"):
            self.avanzar()
            return Cadena(token.valor[1:-1])

        if self.es("BOOLEANO"):
            self.avanzar()
            return Booleano(token.valor == "verdadero")

        if self.es("ID"):
            self.avanzar()
            return Identificador(token.valor, token.linea)

        if self.es("("):
            self.avanzar()
            nodo = self.expresion()
            self.coincidir(")")
            return nodo

        raise SyntaxError(
            f"[Error Sintactico] Se esperaba un valor, "
            f"pero se encontro '{token.valor}' "
            f"en linea {token.linea}."
        )
