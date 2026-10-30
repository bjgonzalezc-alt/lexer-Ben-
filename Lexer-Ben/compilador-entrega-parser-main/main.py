
"""Compilador incremental: Lexer -> Parser -> AST. No ejecuta ni analiza semántica."""
import argparse
from pathlib import Path
from lexer.lexer import Lexer
from parser.parser import Parser

BASE_DIR = Path(__file__).resolve().parent


def analizar_lexico(codigo):
    print('\n=== FASE 1 - ANALISIS LEXICO ===')
    tokens = Lexer(codigo).analizar()
    for token in tokens:
        print(' ', token)
    return tokens


def analizar_sintactico(tokens):
    print('\n=== FASE 2 - ANALISIS SINTACTICO ===')
    arbol = Parser(tokens).parsear()
    print('AST generado:')
    print(arbol)
    return arbol


def main():
    argumentos = argparse.ArgumentParser(description='Lexer + Parser + AST')
    argumentos.add_argument('archivo', nargs='?', default='pruebas/01_basico_valido.txt')
    argumentos.add_argument('--solo-lexer', action='store_true')
    opciones = argumentos.parse_args()
    ruta = Path(opciones.archivo)
    if not ruta.is_absolute() and not ruta.exists():
        ruta = BASE_DIR / ruta
    try:
        codigo = ruta.read_text(encoding='utf-8')
    except OSError as error:
        print(f'No se pudo abrir el archivo: {error}')
        return 1
    print('=== MI COMPILADOR: LEXER + PARSER ===')
    print('\nCODIGO FUENTE:')
    print(codigo)
    try:
        tokens = analizar_lexico(codigo)
        if opciones.solo_lexer:
            print('\nDetenido después del lexer.')
            return 0
        analizar_sintactico(tokens)
        print('\nLa fase semántica está pendiente para la siguiente entrega.')
        return 0
    except NotImplementedError as error:
        print(f'\n[IMPLEMENTACION PENDIENTE] {error}')
        return 2
    except (RuntimeError, SyntaxError, ValueError) as error:
        print(f'\n{error}')
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
