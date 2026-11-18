"""Generación TAC a partir del AST validado de Lexer-Ben."""
import json
from arbol_ast.nodos import Programa, Declaracion, Asignacion, Numero, DecimalLiteral, Cadena, Booleano, Identificador, OpBinaria, OpUnaria, Imprimir, Si, Mientras

class GeneradorTAC:
    def __init__(self):
        self.instrucciones = []
        self.conteo_temp = 0
        self.conteo_etiquetas = 0

    def nuevo_temp(self):
        self.conteo_temp += 1
        return f'@t{self.conteo_temp}'

    def nueva_etiqueta(self):
        self.conteo_etiquetas += 1
        return f'@L{self.conteo_etiquetas}'

    def emitir(self, op, arg1=None, arg2=None, res=None):
        self.instrucciones.append((op, arg1, arg2, res))

    def generar(self, nodo):
        metodo = getattr(self, 'generar_' + type(nodo).__name__, None)
        if metodo is None:
            raise NotImplementedError(f'No hay generador TAC para {type(nodo).__name__}')
        metodo(nodo)
        return self.instrucciones

    def generar_Programa(self, nodo):
        for sentencia in nodo.sentencias:
            self.generar(sentencia)

    def generar_Declaracion(self, nodo):
        self.emitir('ASSIGN', self.evaluar_expr(nodo.expr), None, nodo.id)

    def generar_Asignacion(self, nodo):
        self.emitir('ASSIGN', self.evaluar_expr(nodo.expr), None, nodo.id)

    def generar_Imprimir(self, nodo):
        self.emitir('PRINT', self.evaluar_expr(nodo.expr))

    def generar_Si(self, nodo):
        fin = self.nueva_etiqueta()
        self.emitir('JMP_FALSE', self.evaluar_expr(nodo.condicion), None, fin)
        for sentencia in nodo.bloque_v:
            self.generar(sentencia)
        self.emitir('LABEL', None, None, fin)

    def generar_Mientras(self, nodo):
        inicio, fin = self.nueva_etiqueta(), self.nueva_etiqueta()
        self.emitir('LABEL', None, None, inicio)
        self.emitir('JMP_FALSE', self.evaluar_expr(nodo.condicion), None, fin)
        for sentencia in nodo.bloque:
            self.generar(sentencia)
        self.emitir('JMP', None, None, inicio)
        self.emitir('LABEL', None, None, fin)

    def evaluar_expr(self, nodo):
        if isinstance(nodo, Numero):
            return str(nodo.valor)
        if isinstance(nodo, DecimalLiteral):
            return repr(nodo.valor)
        if isinstance(nodo, Cadena):
            return json.dumps(nodo.valor, ensure_ascii=False)
        if isinstance(nodo, Booleano):
            return 'verdadero' if nodo.valor else 'falso'
        if isinstance(nodo, Identificador):
            return nodo.nombre
        if isinstance(nodo, OpUnaria):
            valor = self.evaluar_expr(nodo.expr)
            destino = self.nuevo_temp()
            self.emitir({'!':'NOT', '-':'NEG', '+':'POS'}[nodo.op], valor, None, destino)
            return destino
        if isinstance(nodo, OpBinaria):
            if nodo.op in ('&&', '||'):
                # Cortocircuito: no evaluar el operando derecho si no es necesario.
                destino = self.nuevo_temp()
                fin = self.nueva_etiqueta()
                izq = self.evaluar_expr(nodo.izq)
                self.emitir('ASSIGN', izq, None, destino)
                if nodo.op == '&&':
                    self.emitir('JMP_FALSE', destino, None, fin)
                else:
                    evaluar_der = self.nueva_etiqueta()
                    self.emitir('JMP_FALSE', destino, None, evaluar_der)
                    self.emitir('JMP', None, None, fin)
                    self.emitir('LABEL', None, None, evaluar_der)
                der = self.evaluar_expr(nodo.der)
                self.emitir('ASSIGN', der, None, destino)
                self.emitir('LABEL', None, None, fin)
                return destino
            izq = self.evaluar_expr(nodo.izq)
            der = self.evaluar_expr(nodo.der)
            destino = self.nuevo_temp()
            self.emitir(nodo.op, izq, der, destino)
            return destino
        raise NotImplementedError(f'Expresión no soportada: {type(nodo).__name__}')
