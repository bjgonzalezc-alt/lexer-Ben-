# Lexer-Ben — Entrega final: TAC y máquina virtual

## Objetivo
Compilador incremental en Python con cinco fases: Lexer, Parser/AST, análisis semántico, generación de código intermedio TAC y ejecución con máquina virtual. Se conservaron las implementaciones personalizadas originales de `lexer/`, `parser/`, `arbol_ast/` y `semantic/`.

## Requisitos
Python 3.10 o superior. No requiere dependencias externas.

## Ejecución
Desde la raíz del repositorio:

```bash
python main.py pruebas/01_basico_valido.txt
python main.py pruebas/22_tac_vm_extensiones.txt
python main.py pruebas/22_tac_vm_extensiones.txt --hasta-tac
python main.py pruebas/22_tac_vm_extensiones.txt --hasta-semantica
python main.py pruebas/22_tac_vm_extensiones.txt --hasta-parser
python main.py pruebas/22_tac_vm_extensiones.txt --solo-lexer
python main.py pruebas/22_tac_vm_extensiones.txt --limite-pasos 10000
python -m unittest discover -s pruebas -v
```

## Cinco métodos TAC implementados
`generar_Asignacion`, `generar_Imprimir`, `generar_Si`, `generar_Mientras` y `evaluar_expr` en `intermediate/tac.py`. Instrucciones: `ASSIGN`, `PRINT`, `JMP`, `JMP_FALSE`, `LABEL`, operaciones binarias y unarias. Temporales `@tN` y etiquetas `@LN`.

## Cuatro métodos VM implementados
`instruccion_operacion`, `instruccion_imprimir`, `instruccion_salto` e `instruccion_salto_condicional` en `vm/maquina_virtual.py`. Se implementa memoria de variables y temporales, saltos por etiquetas, división decimal y límite de pasos.

## Extensión personal integrada
Se conservan literales `decimal`, `cadena`, `booleano`, operadores lógicos `&&`, `||`, `!`, operaciones unarias `+`, `-`, comparaciones `<=`, `>=` y comentarios `//`. En TAC se codifican literales de cadena con JSON para diferenciarlos de identificadores. Los operadores lógicos `&&` y `||` utilizan cortocircuito mediante saltos, por lo que una rama innecesaria no se evalúa. La VM imprime booleanos como `true`/`false` en consola y los conserva como `bool` en memoria.

## Ejemplo TAC y salida VM
Archivo `pruebas/22_tac_vm_extensiones.txt`:

```text
entero contador = 0;
decimal precio = 12.50;
imprimir("Inicio de pruebas");
imprimir(precio);
imprimir(!falso);
imprimir(-3);
si (precio >= 10.0 && verdadero) { imprimir("Precio válido"); }
mientras (contador < 3) { imprimir(contador); contador = contador + 1; }
imprimir(contador == 3 || falso);
```

TAC representativo:

```text
('ASSIGN', '0', None, 'contador')
('ASSIGN', '12.5', None, 'precio')
('PRINT', '"Inicio de pruebas"', None, None)
('>=', 'precio', '10.0', '@t3')
('JMP_FALSE', '@t4', None, '@L2')
('LABEL', None, None, '@L4')
('JMP_FALSE', '@t7', None, '@L5')
('JMP', None, None, '@L4')
```

Salidas esperadas de la VM:

```text
Inicio de pruebas
12.5
true
-3
Precio válido
0
1
2
true
```

## Pruebas y errores
Ejecutar `python -m unittest discover -s pruebas -v`. Las pruebas verifican asignaciones, impresiones, condicionales, bucles, extensiones, cortocircuito, división entre cero, límite de pasos y errores semánticos. Los errores léxicos, sintácticos y semánticos se detectan antes de generar TAC. Una división entre cero genera `ZeroDivisionError`; un bucle sin fin excede `--limite-pasos` y genera `RuntimeError`.

## Archivos principales
- `main.py`: integración de cinco fases y argumentos CLI.
- `intermediate/tac.py`: generador TAC.
- `vm/maquina_virtual.py`: intérprete VM.
- `pruebas/22_tac_vm_extensiones.txt`: evidencia funcional individual.
- `pruebas/test_tac_vm.py`: pruebas automatizadas de la entrega final.
- `pruebas/`: pruebas originales preservadas.

## Entrega GitHub
Subir el contenido de esta carpeta a tu repositorio GitHub original. Verificar desde una clonación limpia que `python -m unittest discover -s pruebas -v` y `python main.py pruebas/22_tac_vm_extensiones.txt` funcionan. La publicación del repositorio debe realizarla el estudiante; este ZIP no constituye un enlace GitHub.
