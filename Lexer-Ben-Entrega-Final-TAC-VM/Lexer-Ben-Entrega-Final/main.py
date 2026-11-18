"""Lexer-Ben: lexer -> parser/AST -> semántica -> TAC -> VM."""
import argparse
from pathlib import Path
from lexer.lexer import Lexer
from parser.parser import Parser
from semantic.analizador import AnalizadorSemantico
from intermediate.tac import GeneradorTAC
from vm.maquina_virtual import MaquinaVirtual

BASE = Path(__file__).resolve().parent

def main():
    ap = argparse.ArgumentParser(description='Compilador Lexer-Ben completo')
    ap.add_argument('archivo', nargs='?', default='pruebas/01_basico_valido.txt')
    ap.add_argument('--solo-lexer', action='store_true')
    ap.add_argument('--hasta-parser', action='store_true')
    ap.add_argument('--hasta-semantica', action='store_true')
    ap.add_argument('--hasta-tac', action='store_true')
    ap.add_argument('--limite-pasos', type=int, default=10000)
    args = ap.parse_args()
    ruta = Path(args.archivo)
    if not ruta.exists(): ruta = BASE / ruta
    try:
        codigo = ruta.read_text(encoding='utf8')
        print('=== FASE 1: LEXER ===')
        tokens = Lexer(codigo).analizar()
        for t in tokens: print(t)
        if args.solo_lexer: return 0
        print('\n=== FASE 2: PARSER Y AST ===')
        ast = Parser(tokens).parsear()
        print(ast)
        if args.hasta_parser: return 0
        print('\n=== FASE 3: SEMÁNTICA ===')
        tabla = AnalizadorSemantico().analizar(ast)
        print('Tabla de símbolos:', tabla)
        if args.hasta_semantica: return 0
        print('\n=== FASE 4: TAC ===')
        tac = GeneradorTAC().generar(ast)
        for i, instruccion in enumerate(tac): print(f'{i:02d} | {instruccion}')
        if args.hasta_tac: return 0
        print('\n=== FASE 5: VM ===')
        vm = MaquinaVirtual(tac)
        vm.ejecutar(args.limite_pasos)
        print('Memoria final:', {k:v for k,v in vm.memoria.items() if not k.startswith('@t')})
        print('Salidas:', vm.salidas)
        return 0
    except (OSError, SyntaxError, RuntimeError, ValueError, NameError, ZeroDivisionError, TypeError, NotImplementedError) as exc:
        print(f'ERROR: {type(exc).__name__}: {exc}')
        return 1

if __name__ == '__main__':
    raise SystemExit(main())
