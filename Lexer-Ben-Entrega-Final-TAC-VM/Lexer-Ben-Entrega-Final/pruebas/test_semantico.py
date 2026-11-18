
import unittest

from lexer.lexer import Lexer
from parser.parser import Parser
from semantic.analizador import (
    AnalizadorSemantico,
    ErrorSemantico
)


def analizar_codigo(codigo):
    tokens = Lexer(codigo).analizar()
    ast = Parser(tokens).parsear()

    analizador = AnalizadorSemantico()
    return analizador.analizar(ast)


class TestAnalisisSemantico(unittest.TestCase):

    def test_declaracion_correcta(self):
        tabla = analizar_codigo("entero edad = 25;")
        self.assertEqual(tabla["edad"]["tipo"], "entero")

    def test_variable_duplicada(self):
        codigo = """
        entero edad = 20;
        entero edad = 30;
        """
        with self.assertRaises(ErrorSemantico):
            analizar_codigo(codigo)

    def test_variable_no_declarada(self):
        with self.assertRaises(ErrorSemantico):
            analizar_codigo("imprimir(edad);")

    def test_tipo_incompatible(self):
        with self.assertRaises(ErrorSemantico):
            analizar_codigo('entero edad = "Benjamin";')

    def test_operacion_aritmetica(self):
        tabla = analizar_codigo(
            "entero resultado = 10 + 5 * 2;"
        )
        self.assertEqual(tabla["resultado"]["tipo"], "entero")

    def test_operacion_incompatible(self):
        with self.assertRaises(ErrorSemantico):
            analizar_codigo(
                "entero resultado = verdadero + 10;"
            )

    def test_condicion_correcta(self):
        codigo = """
        entero edad = 20;
        si (edad >= 18 && verdadero) {
            imprimir("Acceso permitido");
        }
        """
        analizar_codigo(codigo)

    def test_condicion_incorrecta(self):
        codigo = """
        si (10 + 5) {
            imprimir("Hola");
        }
        """
        with self.assertRaises(ErrorSemantico):
            analizar_codigo(codigo)

    def test_decimal(self):
        tabla = analizar_codigo(
            "decimal precio = 15.50;"
        )
        self.assertEqual(tabla["precio"]["tipo"], "decimal")

    def test_extension_logica(self):
        codigo = """
        entero edad = 25;
        si (!(edad < 18) || falso) {
            imprimir("Prueba");
        }
        """
        analizar_codigo(codigo)


if __name__ == "__main__":
    unittest.main(verbosity=2)
