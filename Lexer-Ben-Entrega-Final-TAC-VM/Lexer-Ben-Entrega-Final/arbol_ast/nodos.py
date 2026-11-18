
"""Nodos AST para las estructuras sintácticas del lenguaje."""
from dataclasses import dataclass
from typing import List


class NodoAST:
    pass


@dataclass
class Programa(NodoAST):
    sentencias: List[NodoAST]


@dataclass
class Numero(NodoAST):
    valor: int


@dataclass
class DecimalLiteral(NodoAST):
    valor: float


@dataclass
class Cadena(NodoAST):
    valor: str


@dataclass
class Booleano(NodoAST):
    valor: bool


@dataclass
class Identificador(NodoAST):
    nombre: str
    linea: int


@dataclass
class Declaracion(NodoAST):
    tipo: str
    id: str
    expr: NodoAST
    linea: int


@dataclass
class Asignacion(NodoAST):
    id: str
    expr: NodoAST
    linea: int


@dataclass
class OpBinaria(NodoAST):
    izq: NodoAST
    op: str
    der: NodoAST


@dataclass
class OpUnaria(NodoAST):
    op: str
    expr: NodoAST


@dataclass
class Imprimir(NodoAST):
    expr: NodoAST


@dataclass
class Si(NodoAST):
    condicion: NodoAST
    bloque_v: List[NodoAST]


@dataclass
class Mientras(NodoAST):
    condicion: NodoAST
    bloque: List[NodoAST]
