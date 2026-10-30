
"""Lexer integrado con los tokens adicionales del proyecto."""
import re
from typing import List
from .token import Token


class Lexer:
    def __init__(self, codigo_fuente: str):
        self.codigo = codigo_fuente
        self.tokens: List[Token] = []

        self.esquema_tokens = [
            # Palabras reservadas
            ('PR_ENTERO', r'\bentero\b'),
            ('PR_DECIMAL', r'\bdecimal\b'),
            ('PR_SI', r'\bsi\b'),
            ('PR_MIENTRAS', r'\bmientras\b'),
            ('PR_IMPRIMIR', r'\bimprimir\b'),

            # Valores
            ('BOOLEANO', r'\b(?:verdadero|falso)\b'),
            ('DECIMAL', r'\d+\.\d+'),
            ('NUMERO', r'\d+'),
            ('CADENA', r'"[^"\n]*"|\'[^\'\n]*\''),

# Identificadores y operadores
('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),
('OP_REL', r'==|!=|<=|>=|<|>'),
('OP_LOGICO', r'&&|\|\||!'),

# Comentarios antes del operador /
('COMENTARIO', r'//[^\r\n]*'),

('OP_ARIT', r'[+\-*/]'),
('ASIGNACION', r'='),

# Delimitadores y control de espacios
('DELIM', r'[();{}]'),
('ESPACIO', r'[ \t]+'),
('NUEVA_LINEA', r'\r\n|\n|\r'),
('ERROR', r'.'),    
        ]

        self.regex_maestro = re.compile('|'.join(
            f'(?P<{nombre}>{patron})'
            for nombre, patron in self.esquema_tokens
        ))

    def analizar(self) -> List[Token]:
        self.tokens = []
        numero_linea = 1

        for match in self.regex_maestro.finditer(self.codigo):
            tipo, valor = match.lastgroup, match.group()

            if tipo == 'NUEVA_LINEA':
                numero_linea += 1
            elif tipo in ('ESPACIO', 'COMENTARIO'):
                continue
            elif tipo == 'ERROR':
                raise RuntimeError(
                    f"[Error Lexico] Caracter inesperado '{valor}' "
                    f"en linea {numero_linea}"
                )
            else:
                self.tokens.append(Token(tipo, valor, numero_linea))

        self.tokens.append(Token('EOF', '', numero_linea))
        return self.tokens
