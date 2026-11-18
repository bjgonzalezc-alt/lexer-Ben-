import unittest
from lexer.lexer import Lexer
from parser.parser import Parser
from semantic.analizador import AnalizadorSemantico
from intermediate.tac import GeneradorTAC
from vm.maquina_virtual import MaquinaVirtual


def ejecutar(codigo, limite=10000):
    ast = Parser(Lexer(codigo).analizar()).parsear()
    AnalizadorSemantico().analizar(ast)
    tac = GeneradorTAC().generar(ast)
    vm = MaquinaVirtual(tac)
    return tac, vm.ejecutar(limite)

class TestTacVm(unittest.TestCase):
    def test_asignacion_y_salida(self):
        _, salida = ejecutar('entero x = 2; x = x + 3; imprimir(x);')
        self.assertEqual(salida, [5])
    def test_condicional(self):
        _, salida = ejecutar('entero x = 2; si (x > 1) { imprimir(9); }')
        self.assertEqual(salida, [9])
    def test_bucle(self):
        _, salida = ejecutar('entero x = 0; mientras (x < 3) { imprimir(x); x = x + 1; }')
        self.assertEqual(salida, [0, 1, 2])
    def test_extensiones(self):
        _, salida = ejecutar('decimal x = 2.5; imprimir(x); imprimir("hola"); imprimir(!falso); imprimir(-3);')
        self.assertEqual(salida, [2.5, 'hola', True, -3])
    def test_cortocircuito(self):
        _, salida = ejecutar('si (falso && (1 / 0 > 0)) { imprimir(1); } imprimir(2);')
        self.assertEqual(salida, [2])
    def test_division_cero(self):
        with self.assertRaises(ZeroDivisionError): ejecutar('imprimir(1 / 0);')
    def test_limite(self):
        with self.assertRaises(RuntimeError): ejecutar('mientras (verdadero) { imprimir(1); }', 15)
    def test_error_semantico(self):
        with self.assertRaises(Exception): ejecutar('imprimir(no_existe);')

if __name__ == '__main__': unittest.main()
