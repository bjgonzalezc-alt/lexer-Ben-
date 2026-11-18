
"""Analizador semántico del compilador."""

from arbol_ast.nodos import (
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


class ErrorSemantico(Exception):
    """Excepción para errores encontrados durante el análisis semántico."""
    pass


class AnalizadorSemantico:

    def __init__(self):
        self.tabla_simbolos = {}

    def analizar(self, programa):
        """Inicia el análisis semántico de un programa."""
        self.tabla_simbolos = {}
        self.visitar(programa)
        return self.tabla_simbolos

    def visitar(self, nodo):

        if isinstance(nodo, Programa):
            for sentencia in nodo.sentencias:
                self.visitar(sentencia)

        elif isinstance(nodo, Declaracion):
            self.declaracion(nodo)

        elif isinstance(nodo, Asignacion):
            self.asignacion(nodo)

        elif isinstance(nodo, Imprimir):
            return self.visitar(nodo.expr)

        elif isinstance(nodo, Si):
            tipo = self.visitar(nodo.condicion)

            if tipo != "booleano":
                raise ErrorSemantico(
                    "La condición de 'si' debe ser de tipo booleano."
                )

            for sentencia in nodo.bloque_v:
                self.visitar(sentencia)

        elif isinstance(nodo, Mientras):
            tipo = self.visitar(nodo.condicion)

            if tipo != "booleano":
                raise ErrorSemantico(
                    "La condición de 'mientras' debe ser de tipo booleano."
                )

            for sentencia in nodo.bloque:
                self.visitar(sentencia)

        elif isinstance(nodo, Numero):
            return "entero"

        elif isinstance(nodo, DecimalLiteral):
            return "decimal"

        elif isinstance(nodo, Cadena):
            return "cadena"

        elif isinstance(nodo, Booleano):
            return "booleano"

        elif isinstance(nodo, Identificador):
            if nodo.nombre not in self.tabla_simbolos:
                raise ErrorSemantico(
                    f"La variable '{nodo.nombre}' no ha sido declarada. "
                    f"Linea {nodo.linea}."
                )

            return self.tabla_simbolos[nodo.nombre]["tipo"]

        elif isinstance(nodo, OpUnaria):
            tipo = self.visitar(nodo.expr)

            if nodo.op == "!":
                if tipo != "booleano":
                    raise ErrorSemantico(
                        "El operador '!' requiere un valor booleano."
                    )
                return "booleano"

            if nodo.op in ("+", "-"):
                if tipo not in ("entero", "decimal"):
                    raise ErrorSemantico(
                        f"El operador '{nodo.op}' requiere un valor numérico."
                    )
                return tipo

        elif isinstance(nodo, OpBinaria):
            return self.operacion(nodo)

        else:
            raise ErrorSemantico(
                f"Nodo no reconocido: {type(nodo).__name__}"
            )

    def declaracion(self, nodo):
        """Registra una variable y verifica su tipo."""

        if nodo.id in self.tabla_simbolos:
            raise ErrorSemantico(
                f"La variable '{nodo.id}' ya fue declarada. "
                f"Linea {nodo.linea}."
            )

        tipo_expr = self.visitar(nodo.expr)

        if tipo_expr != nodo.tipo:
            raise ErrorSemantico(
                f"No se puede asignar un valor de tipo '{tipo_expr}' "
                f"a la variable '{nodo.id}' de tipo '{nodo.tipo}'."
            )

        self.tabla_simbolos[nodo.id] = {
            "tipo": nodo.tipo,
            "valor": "inicializado"
        }

    def asignacion(self, nodo):
        """Verifica que una variable exista y reciba un tipo compatible."""

        if nodo.id not in self.tabla_simbolos:
            raise ErrorSemantico(
                f"La variable '{nodo.id}' no ha sido declarada. "
                f"Linea {nodo.linea}."
            )

        tipo_variable = self.tabla_simbolos[nodo.id]["tipo"]
        tipo_expr = self.visitar(nodo.expr)

        if tipo_variable != tipo_expr:
            raise ErrorSemantico(
                f"No se puede asignar un valor de tipo '{tipo_expr}' "
                f"a la variable '{nodo.id}' de tipo '{tipo_variable}'."
            )

        self.tabla_simbolos[nodo.id]["valor"] = "inicializado"

    def operacion(self, nodo):
        """Comprueba los tipos de las operaciones binarias."""

        tipo_izq = self.visitar(nodo.izq)
        tipo_der = self.visitar(nodo.der)
        operador = nodo.op

        # Operaciones aritméticas
        if operador in ("+", "-", "*", "/"):

            if tipo_izq not in ("entero", "decimal") or \
               tipo_der not in ("entero", "decimal"):
                raise ErrorSemantico(
                    f"Operación incompatible: el operador '{operador}' "
                    "requiere operandos numéricos."
                )

            if operador == "/" or \
               tipo_izq == "decimal" or tipo_der == "decimal":
                return "decimal"

            return "entero"

        # Operaciones relacionales
        if operador in ("==", "!=", "<", ">", "<=", ">="):

            if operador in ("<", ">", "<=", ">="):
                if tipo_izq not in ("entero", "decimal") or \
                   tipo_der not in ("entero", "decimal"):
                    raise ErrorSemantico(
                        f"El operador '{operador}' requiere operandos numéricos."
                    )

            elif tipo_izq != tipo_der and not (
                tipo_izq in ("entero", "decimal")
                and tipo_der in ("entero", "decimal")
            ):
                raise ErrorSemantico(
                    f"Tipos incompatibles en la comparación '{operador}'."
                )

            return "booleano"

        # Operaciones lógicas
        if operador in ("&&", "||"):

            if tipo_izq != "booleano" or tipo_der != "booleano":
                raise ErrorSemantico(
                    f"El operador '{operador}' requiere operandos booleanos."
                )

            return "booleano"

        raise ErrorSemantico(
            f"Operador no reconocido: '{operador}'."
        )
