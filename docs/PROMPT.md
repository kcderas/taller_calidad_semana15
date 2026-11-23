# Prompt maestro utilizado

Durante el desarrollo de este taller se usó un asistente de IA como apoyo. Se
documenta aquí la instrucción empleada, junto con las decisiones de diseño que
se tomaron y los criterios con que se revisó el resultado.

---

## Instrucción entregada al asistente

> Necesito un proyecto en Python que cumpla estándares profesionales de
> software. No quiero un script suelto: quiero un proyecto versionable,
> documentado y con pruebas.
>
> **Estructura requerida**
>
> ```
> taller_calidad_semana15/
> ├── data/          # datos de entrada, NO versionados
> ├── src/           # código fuente
> ├── tests/         # pruebas unitarias
> ├── .gitignore
> ├── requirements.txt
> └── README.md
> ```
>
> Incluí `__init__.py` en `src/` y `tests/` para que Python los trate como
> paquetes, y un `.gitkeep` en `data/` para que Git conserve la carpeta aunque
> su contenido esté excluido.
>
> **Separación de responsabilidades**
>
> - `src/procesamiento.py` contiene únicamente lógica de negocio: recibe un
>   `DataFrame` y devuelve estructuras de Python. No lee archivos, no imprime,
>   no se conecta a nada. Esa independencia es lo que permite probarlo de forma
>   aislada.
> - `src/main.py` es el punto de entrada: lee el archivo, llama a la lógica y
>   muestra el resultado.
>
> **Función principal**
>
> `calcular_metricas_ventas(dataframe)` debe devolver un diccionario con
> `num_transacciones`, `total_ventas`, `total_ganancias`, `ticket_promedio` y
> `margen_porcentual`, a partir de las columnas `region`, `categoria`, `ventas`
> y `ganancias`.
>
> Comportamiento esperado en los bordes:
>
> - Un `DataFrame` **vacío** es entrada válida, no un error: devuelve métricas
>   en cero. Un período sin movimientos es un escenario de negocio legítimo y
>   el reporte debe poder generarse igual.
> - Una **columna faltante** sí es un error de contrato: levanta `ValueError`
>   con un mensaje que indique qué falta.
> - Un argumento que no sea `DataFrame` levanta `TypeError`.
> - `ticket_promedio` y `margen_porcentual` valen `0.0` cuando no hay datos, en
>   lugar de `NaN` o `ZeroDivisionError`.
> - Las filas con nulos en las columnas numéricas se descartan antes de agregar.
>
> **Documentación**
>
> Docstrings estilo Google en todas las funciones y en el módulo: propósito,
> `Args` con tipos, `Returns`, `Raises` y al menos un `Examples`. El `README.md`
> debe cubrir qué hace el proyecto, la estructura de carpetas, el formato
> esperado de los datos, instalación, uso, cómo correr las pruebas y las
> decisiones de diseño no obvias.
>
> **Pruebas**
>
> Con `pytest`, cubriendo tres escenarios: **normal** (totales conocidos
> calculados a mano), **vacío** y **inválido**. Las pruebas construyen sus
> propios datos; no dependen de archivos en disco ni del orden de ejecución.
>
> **Exclusiones y dependencias**
>
> El `.gitignore` debe excluir `__pycache__/`, `*.pyc`, `.venv/`,
> `.pytest_cache/`, `*.csv` y `.env`, conservando `.env.example`. El
> `requirements.txt` lleva versiones fijadas, no nombres sueltos: sin versión,
> cada entorno instala algo distinto y el proyecto deja de ser reproducible.
>
> Ninguna credencial debe aparecer en el código. `.env.example` documenta qué
> variables hacen falta, con valores ficticios.

---

## Decisiones propias tomadas sobre la salida del asistente

| Decisión | Razón |
|---|---|
| Un `DataFrame` vacío devuelve ceros en lugar de levantar excepción | Un período sin ventas es un caso de negocio real, no una falla |
| Una columna faltante sí levanta `ValueError` | Es un incumplimiento del contrato de la función, no un dato ausente |
| `main.py` separado de `procesamiento.py` | Mantener la lógica libre de entrada/salida es lo que la hace verificable |
| Versiones fijadas en `requirements.txt` | Garantizar que el entorno sea reproducible en otra máquina |
| Excepción `!data/ventas_ejemplo.csv` en el `.gitignore` | Una muestra ficticia pequeña documenta el formato esperado; el resto de CSV queda excluido |
| Se agregó `.env.example` | Deja constancia de qué variables requiere el proyecto sin exponer valores reales |

---

## Verificación realizada

1. `pytest -v` → 9 pruebas en verde, sin advertencias.
2. `python -m src.main` → ejecución correcta sobre el archivo de ejemplo.
3. `git status` revisado **antes** del primer commit, para confirmar que
   `.venv/`, `__pycache__/` y `.pytest_cache/` quedaran fuera del historial.
4. Historial construido en seis commits siguiendo *Conventional Commits*
   (`chore`, `build`, `feat`, `test`, `docs`), de modo que el log refleje el
   proceso y no una carga única.
