# MiCompilador — Entrega Lexer + Parser + AST

Este proyecto es una **base para completar**, no un parser resuelto. El objetivo es integrar el **lexer que ya desarrollaste** con un analizador sintáctico que genere un AST. No incluye análisis semántico, TAC ni máquina virtual.

## Contenido proporcionado por el docente

- `main.py`: punto de entrada del compilador. Llama al lexer y después al parser.
- `lexer/token.py`: clase `Token(tipo, valor, linea)`.
- `lexer/lexer.py`: lexer base funcional **de referencia**.
- `arbol_ast/nodos.py`: clases de AST (`Programa`, `Declaracion`, `Asignacion`, `Numero`, `Identificador`, `OpBinaria`, `Si`, `Mientras`, `Imprimir`).
- `parser/parser.py`: clase `Parser`, atributos de control, `avanzar()` y `coincidir()` completos, y 12 métodos marcados con `TODO`.
- `pruebas/`: archivos para probar casos válidos, errores y precedencia; tests de Python.

**IMPORTANTE:** reemplaza el lexer de referencia con **tu propio lexer de la entrega anterior** y CONSERVA todos los tokens adicionales que implementaste. Asegúrate de que `Lexer(codigo).analizar()` produzca una lista de `Token` y termine con `EOF`.

## Estructura

```text
MiCompilador/
├── main.py
├── lexer/
│   ├── __init__.py
│   ├── token.py
│   └── lexer.py
├── parser/
│   ├── __init__.py
│   └── parser.py           ← COMPLETAR TODO
├── arbol_ast/
│   ├── __init__.py
│   └── nodos.py
└── pruebas/
    ├── 01_basico_valido.txt
    ├── 02_expresiones.txt
    ├── 03_control.txt
    ├── 04_error_falta_punto_coma.txt
    ├── 05_error_declaracion.txt
    ├── 06_solo_error_semantico_futuro.txt
    ├── 07_token_personalizado_EDITAR.txt
    └── test_integracion.py
```

La carpeta `arbol_ast` se llama así, en lugar de `ast`, para evitar colisiones con el **módulo estándar `ast` de Python**.

## Cómo ejecutar

No hay dependencias de terceros (Python 3.10 o superior). Desde la raíz del proyecto:

```bash
python main.py --solo-lexer
python main.py
python main.py pruebas/02_expresiones.txt
python main.py pruebas/04_error_falta_punto_coma.txt
```

Al principio, `python main.py` imprime los tokens y `[IMPLEMENTACION PENDIENTE] TODO 1 ...`. Esto es **intencional**: el parser aún no está implementado.

## Trabajo del estudiante: cuatro bloques

### A. Declaraciones y asignaciones
Completar en `parser/parser.py`: `parsear()`, `sentencia()`, `declaracion()`, `asignacion()`.

**Ejemplo:** `entero edad = 20; edad = 21;` debe producir un `Programa` con dos sentencias AST. Para reconocer un token, usa `coincidir('PR_ENTERO')`, `coincidir('ID')`, `coincidir('=')` o `coincidir(';')`, según corresponda. `coincidir()` acepta **tipo o valor**.

**Para probar primero la parte A:** una versión inicial de `factor()` puede leer únicamente `NUMERO` e `ID`, mientras `expresion()`, `aritmetica()` y `termino()` delegan a su siguiente nivel. Después amplía estos métodos con operadores en la parte B. Así no necesitas terminar toda la precedencia para probar la declaración sencilla.

### B. Expresiones y precedencia
Completar `expresion()`, `aritmetica()`, `termino()`, `factor()`. Para `5 + 3 * 2` se espera un nodo `OpBinaria` con `op = "+"` cuya rama derecha sea la multiplicación, no una suma y luego una multiplicación al mismo nivel.

### C. Sentencias y control
Completar `sentencia_imprimir()`, `sentencia_si()`, `sentencia_mientras()`, `bloque()`, e integrar esas opciones en `sentencia()`.

### D. Tokens adicionales de tu lexer
Debes **adaptar el parser a tu extensión personal** cuando afecte a la sintaxis. Por ejemplo:

| Token previo | Cambio posible |
|---|---|
| `%` con tipo `OP_MOD` | Agregar `%` a `termino()` y representar la operación en `OpBinaria`. |
| `DECIMAL` | Reconocerlo en `factor()` y definir cómo se verá en el AST. |
| `sino` | Añadir la rama al parser y adaptar la clase `Si` o crear un nodo. |
| `&&`, `||` | Agregar niveles de precedencia al parser. |
| `<=` / `>=` como `OP_REL` | La regla por categoría `OP_REL` ya puede cubrirlos; verificarlo con pruebas. |
| Comentario `//` descartado por el lexer | No es necesario enviarlo al parser. |

**Que el lexer reconozca un token NO garantiza que el parser admita su uso en el código fuente.** Debes probar una cadena válida y una inválida con tu extensión. Si no requiere cambio en el parser, explica la razón.

## Gramática base orientativa

```text
programa    → sentencia* EOF
sentencia   → declaracion | asignacion | imprimir | si | mientras
declaracion → 'entero' ID '=' expresion ';'
asignacion  → ID '=' expresion ';'
imprimir    → 'imprimir' '(' expresion ')' ';'
si          → 'si' '(' expresion ')' bloque
mientras    → 'mientras' '(' expresion ')' bloque
bloque      → '{' sentencia* '}'
expresion   → aritmetica (OP_REL aritmetica)*
aritmetica  → termino (('+' | '-') termino)*
termino     → factor (('*' | '/') factor)*
factor      → NUMERO | ID | '(' expresion ')'
```

## Comprobar avances

```bash
python -m unittest pruebas.test_integracion.TestLexer
python -m unittest pruebas.test_integracion.TestParserBasico
python -m unittest pruebas.test_integracion.TestExpresiones
python -m unittest pruebas.test_integracion.TestControl
python -m unittest pruebas.test_integracion.TestErrores
```

Las pruebas del parser fallarán mientras queden métodos pendientes: **es normal** y permite revisar cada etapa por separado. No cambies los casos de prueba para ocultar errores.

## Diferencia fundamental con semántica

`entero x = ;` contiene tokens reconocibles, pero es **sintácticamente inválido**. En cambio, `x = 10;` es **sintácticamente válido**, aunque `x` no esté declarada: esa validación corresponde a la próxima fase (**semántica**). No implemente tabla de símbolos ni validaciones de tipos en esta etapa.

## Entregable

Subir el proyecto actualizado a GitHub. Presentar evidencia de: integración con el lexer propio, AST correcto, detección de error sintáctico y prueba de la extensión personal. La semántica queda pendiente.
