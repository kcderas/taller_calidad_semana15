# Taller de Calidad — Semana 15

Proyecto del taller *Del Script al Producto de Ingeniería*. Toma un conjunto
de transacciones de venta y calcula métricas agregadas, siguiendo prácticas
de estructura modular, documentación y pruebas automatizadas.

---

## Qué hace

A partir de un archivo CSV de transacciones, el proyecto calcula:

| Métrica | Descripción |
|---|---|
| `num_transacciones` | Cantidad de registros válidos |
| `total_ventas` | Suma de la columna `ventas` |
| `total_ganancias` | Suma de la columna `ganancias` |
| `ticket_promedio` | Venta promedio por transacción |
| `margen_porcentual` | Ganancias sobre ventas, en porcentaje |

Adicionalmente genera un detalle agrupado por región y categoría.

---

## Estructura del proyecto

```text
taller_calidad_semana15/
├── data/                       # Datos de entrada (no versionados)
│   └── ventas_ejemplo.csv      # Muestra ficticia que documenta el formato
├── src/                        # Código fuente
│   ├── __init__.py
│   ├── procesamiento.py        # Lógica de negocio: cálculo de métricas
│   └── main.py                 # Punto de entrada: lee el archivo e imprime
├── tests/                      # Pruebas unitarias
│   ├── __init__.py
│   └── test_procesamiento.py
├── .env.example                # Plantilla de variables de entorno
├── .gitignore
├── requirements.txt
└── README.md
```

**Criterio de separación:** `procesamiento.py` no lee archivos ni imprime nada;
recibe un `DataFrame` y devuelve estructuras de Python. Esa separación es lo
que permite probarlo de forma aislada, sin depender de rutas ni de la consola.
`main.py` se encarga de la entrada/salida y delega el cálculo.

---

## Formato de los datos

El archivo CSV debe tener estas cuatro columnas:

| Columna | Tipo | Descripción |
|---|---|---|
| `region` | texto | Región geográfica de la venta |
| `categoria` | texto | Categoría del producto |
| `ventas` | decimal | Importe de la venta |
| `ganancias` | decimal | Ganancia asociada a esa venta |

Las filas con valores nulos en `ventas` o `ganancias` se descartan antes de
agregar, para que un registro incompleto no distorsione los totales.

---

## Instalación

Requiere Python 3.9 o superior.

```bash
# 1. Crear y activar un entorno virtual
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# Linux / macOS
source .venv/bin/activate

# 2. Instalar dependencias
pip install -r requirements.txt
```

---

## Uso

```bash
# Con el archivo de ejemplo incluido
python -m src.main

# Con otro archivo
python -m src.main data/mis_ventas.csv
```

Desde Python:

```python
import pandas as pd
from src.procesamiento import calcular_metricas_ventas

ventas = pd.read_csv("data/ventas_ejemplo.csv")
metricas = calcular_metricas_ventas(ventas)
print(metricas["total_ventas"])
```

---

## Pruebas

```bash
pytest -v
```

Se cubren tres escenarios:

| Caso | Qué verifica |
|---|---|
| **Normal** | Totales, ticket promedio, margen y agrupación con datos conocidos |
| **Vacío** | Un `DataFrame` sin registros devuelve ceros, no una excepción ni `NaN` |
| **Inválido** | Falta de columnas obligatorias o tipo incorrecto fallan de forma explícita |

**Decisión de diseño:** un conjunto vacío se trata como entrada válida y no
como error. Un período sin movimientos es un escenario de negocio legítimo, y
el reporte debe poder generarse igual. En cambio, una columna faltante sí es un
error del contrato y levanta `ValueError`.

---

## Seguridad y manejo de datos

- Las credenciales nunca se escriben en el código. Se leen de variables de
  entorno; `.env.example` documenta cuáles hacen falta, con valores ficticios.
- `.env` está excluido del versionado mediante `.gitignore`.
- Los archivos `.csv` no se versionan por defecto. La única excepción
  intencional es `data/ventas_ejemplo.csv`, una muestra ficticia generada para
  documentar el formato esperado.

---

## Dependencias

| Paquete | Uso |
|---|---|
| `pandas` | Manipulación y agregación de datos tabulares |
| `pytest` | Ejecución de las pruebas unitarias |
