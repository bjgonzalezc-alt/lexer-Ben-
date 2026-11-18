"""Intérprete de TAC de Lexer-Ben, con límite de pasos y tipos Python."""
import json

OPERADORES = {'+', '-', '*', '/', '==', '!=', '<', '>', '<=', '>='}

class MaquinaVirtual:
    def __init__(self, tac):
        self.tac = list(tac)
        self.memoria = {}
        self.ip = 0
        self.salidas = []
        self.etiquetas = {}
        for i, (op, a, b, res) in enumerate(self.tac):
            if op == 'LABEL':
                if not res or res in self.etiquetas:
                    raise ValueError(f'Etiqueta inválida o duplicada: {res}')
                self.etiquetas[res] = i

    def obtener_val(self, arg):
        if arg is None:
            raise ValueError('Operando obligatorio ausente')
        if arg in self.memoria:
            return self.memoria[arg]
        if arg == 'verdadero':
            return True
        if arg == 'falso':
            return False
        if arg.startswith('"'):
            return json.loads(arg)
        try:
            return int(arg)
        except ValueError:
            try:
                return float(arg)
            except ValueError:
                raise NameError(f'Variable o temporal sin valor: {arg}')

    def instruccion_asignar(self, fuente, destino):
        if not destino:
            raise ValueError('ASSIGN sin destino')
        self.memoria[destino] = self.obtener_val(fuente)

    def instruccion_operacion(self, op, arg1, arg2, res):
        if not res:
            raise ValueError('Operación sin destino')
        a, b = self.obtener_val(arg1), self.obtener_val(arg2)
        if op == '+': valor = a + b
        elif op == '-': valor = a - b
        elif op == '*': valor = a * b
        elif op == '/':
            if b == 0: raise ZeroDivisionError('División entre cero')
            valor = a / b
        elif op == '==': valor = a == b
        elif op == '!=': valor = a != b
        elif op == '<': valor = a < b
        elif op == '>': valor = a > b
        elif op == '<=': valor = a <= b
        elif op == '>=': valor = a >= b
        else: raise NotImplementedError(f'Operador desconocido: {op}')
        self.memoria[res] = valor

    def instruccion_imprimir(self, fuente):
        valor = self.obtener_val(fuente)
        self.salidas.append(valor)
        print('>> SALIDA:', str(valor).lower() if isinstance(valor, bool) else valor)

    def _ubicacion_etiqueta(self, etiqueta):
        if etiqueta not in self.etiquetas:
            raise ValueError(f'Etiqueta inexistente: {etiqueta}')
        return self.etiquetas[etiqueta]

    def instruccion_salto(self, etiqueta):
        self.ip = self._ubicacion_etiqueta(etiqueta)

    def instruccion_salto_condicional(self, condicion, etiqueta):
        if not self.obtener_val(condicion):
            self.ip = self._ubicacion_etiqueta(etiqueta)

    def ejecutar(self, max_pasos=10000):
        if max_pasos < 1: raise ValueError('max_pasos debe ser positivo')
        pasos = 0
        while 0 <= self.ip < len(self.tac):
            if pasos >= max_pasos:
                raise RuntimeError(f'Límite de ejecución: {max_pasos} pasos')
            pasos += 1
            op, a, b, res = self.tac[self.ip]
            if op == 'ASSIGN': self.instruccion_asignar(a, res)
            elif op in OPERADORES: self.instruccion_operacion(op, a, b, res)
            elif op == 'PRINT': self.instruccion_imprimir(a)
            elif op == 'JMP': self.instruccion_salto(res)
            elif op == 'JMP_FALSE': self.instruccion_salto_condicional(a, res)
            elif op == 'LABEL': pass
            elif op in ('NOT', 'NEG', 'POS'):
                if not res: raise ValueError(f'{op} sin destino')
                valor = self.obtener_val(a)
                self.memoria[res] = {'NOT': lambda: not valor, 'NEG': lambda: -valor, 'POS': lambda: +valor}[op]()
            else: raise NotImplementedError(f'Instrucción VM no soportada: {op}')
            self.ip += 1
        return self.salidas
