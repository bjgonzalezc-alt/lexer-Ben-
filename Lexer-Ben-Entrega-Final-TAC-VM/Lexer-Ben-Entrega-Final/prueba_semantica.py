from semantic.analizador import AnalizadorSemantico
from lexer.lexer import Lexer
from parser.parser import Parser

codigo = 'entero edad = "hola";'

ast = Parser(Lexer(codigo).analizar()).parsear()
resultado = AnalizadorSemantico().analizar(ast)

print(resultado)
