\# MiCompilador — Lexer + Parser + AST + Análisis Semántico



\## Descripción



Proyecto de compilador incremental desarrollado en Python. Parte de la integración del analizador léxico propio, el analizador sintáctico y el Árbol de Sintaxis Abstracta (AST), desarrollados en entregas anteriores.



En esta etapa se incorpora el análisis semántico para verificar la validez de las declaraciones, variables, tipos de datos, operaciones y condiciones del lenguaje.



\## Objetivo



Continuar el desarrollo del compilador conservando los componentes implementados anteriormente e integrando una nueva fase de análisis semántico.



El compilador procesa el código fuente mediante tres fases:



1\. Análisis léxico (Lexer).

2\. Análisis sintáctico (Parser y generación del AST).

3\. Análisis semántico (validación de reglas del lenguaje).



\## Componentes del proyecto



\- \*\*Lexer:\*\* reconoce los tokens del código fuente y conserva las extensiones implementadas en la entrega anterior.

\- \*\*Parser:\*\* verifica la estructura sintáctica de las instrucciones.

\- \*\*AST:\*\* representa el programa mediante nodos como declaraciones, asignaciones, operaciones y estructuras de control.

\- \*\*Analizador semántico:\*\* recorre el AST y comprueba la compatibilidad de tipos, declaraciones, variables y condiciones.



\## Características del lenguaje



El lenguaje contempla:



\- Declaración y asignación de variables.

\- Tipos de datos: `entero`, `decimal`, `cadena` y `booleano`.

\- Operaciones aritméticas: `+`, `-`, `\*` y `/`.

\- Operadores relacionales: `==`, `!=`, `<`, `>`, `<=` y `>=`.

\- Operadores lógicos: `\&\&`, `||` y `!`.

\- Estructuras condicionales: `si`.

\- Ciclos: `mientras`.

\- Instrucciones de salida: `imprimir`.



\### Extensiones personales



Se conservan las características adicionales del lenguaje desarrolladas en las entregas anteriores. En esta etapa se incorporan sus respectivas validaciones semánticas cuando corresponde.



Los operadores lógicos, los valores decimales y booleanos cuentan con reglas de validación de tipos. Los comentarios descartados por el Lexer no requieren procesamiento adicional en el Parser ni en el analizador semántico.



\## Análisis semántico



El analizador semántico valida las reglas del lenguaje mediante el recorrido del AST.



Entre sus verificaciones se encuentran:



\- Evitar declaraciones duplicadas.

\- Detectar el uso de variables no declaradas.

\- Comprobar la compatibilidad de tipos en declaraciones y asignaciones.

\- Validar operaciones aritméticas, relacionales y lógicas.

\- Comprobar que las condiciones de `si` y `mientras` sean booleanas.



\### Tabla de símbolos



La tabla de símbolos almacena información de las variables declaradas durante el análisis.



| Campo | Descripción |

|---|---|

| Nombre | Identificador de la variable. |

| Tipo | Tipo de dato declarado. |

| Valor | Estado de inicialización. |



Ejemplo:



Código fuente:



```text

entero edad = 20;

edad = 21;

```



Resultado:



```python

{

&#x20;   "edad": {

&#x20;       "tipo": "entero",

&#x20;       "valor": "inicializado"

&#x20;   }

}

```



\## Estructura del proyecto



```text

MiCompilador/

├── main.py

├── lexer/

│   ├── \_\_init\_\_.py

│   ├── token.py

│   └── lexer.py

├── parser/

│   ├── \_\_init\_\_.py

│   └── parser.py

├── arbol\_ast/

│   ├── \_\_init\_\_.py

│   └── nodos.py

├── semantic/

│   └── analizador.py

├── pruebas/

│   ├── test\_integracion.py

│   └── test\_semantico.py

└── README.md

```



\## Requisitos



\- Python 3.10 o superior.

\- No requiere dependencias externas de terceros.



\## Ejecución



Desde la carpeta raíz del proyecto:



Ejecutar el compilador completo:



```bash

python main.py

```



Ejecutar con un archivo específico:



```bash

python main.py pruebas/01\_basico\_valido.txt

```



Ejecutar solamente el Lexer:



```bash

python main.py --solo-lexer

```



\## Pruebas



Ejecutar todas las pruebas:



```bash

python -m unittest discover -v

```



Ejecutar las pruebas de integración:



```bash

python -m unittest pruebas.test\_integracion -v

```



Ejecutar las pruebas semánticas:



```bash

python -m unittest pruebas.test\_semantico -v

```



\## Resultados de las pruebas



Durante la validación del proyecto se obtuvieron los siguientes resultados:



| Categoría | Pruebas aprobadas |

|---|---:|

| Lexer, Parser y AST | 14 |

| Análisis semántico | 10 |

| \*\*Total\*\* | \*\*24\*\* |



Todas las pruebas ejecutadas finalizaron correctamente.



\## Conclusión



El compilador integra las fases léxica, sintáctica y semántica, conservando los componentes desarrollados en las entregas anteriores. La incorporación del análisis semántico permite detectar errores relacionados con variables, declaraciones, tipos de datos, operaciones y condiciones, además de generar una tabla de símbolos con la información de las variables declaradas.



