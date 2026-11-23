"""Punto de entrada del proyecto.

Se encarga únicamente de leer el archivo de datos y mostrar el resultado.
Toda la lógica de negocio vive en :mod:`src.procesamiento`, de modo que pueda
probarse sin depender de archivos ni de la consola.

Uso:
    python -m src.main
    python -m src.main data/otro_archivo.csv
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

from src.procesamiento import calcular_metricas_ventas, resumen_por_region

RUTA_POR_DEFECTO = Path("data") / "ventas_ejemplo.csv"


def cargar_ventas(ruta: Path) -> pd.DataFrame:
    """Lee un archivo CSV de transacciones de venta.

    Args:
        ruta (pathlib.Path): Ubicación del archivo CSV a leer.

    Returns:
        pandas.DataFrame: Contenido del archivo sin transformar.

    Raises:
        FileNotFoundError: Si la ruta indicada no existe.
    """
    if not ruta.is_file():
        raise FileNotFoundError(f"No se encontró el archivo de datos: {ruta}")
    return pd.read_csv(ruta)


def main() -> None:
    """Ejecuta el flujo completo: cargar, calcular y mostrar.

    Returns:
        None: Escribe el resultado en la salida estándar.
    """
    ruta = Path(sys.argv[1]) if len(sys.argv) > 1 else RUTA_POR_DEFECTO
    ventas = cargar_ventas(ruta)

    metricas = calcular_metricas_ventas(ventas)

    print(f"Archivo procesado: {ruta}")
    print("-" * 46)
    print(f"Transacciones      : {metricas['num_transacciones']:>12,}")
    print(f"Total de ventas    : {metricas['total_ventas']:>12,.2f}")
    print(f"Total de ganancias : {metricas['total_ganancias']:>12,.2f}")
    print(f"Ticket promedio    : {metricas['ticket_promedio']:>12,.2f}")
    print(f"Margen             : {metricas['margen_porcentual']:>11,.2f} %")
    print("-" * 46)
    print("\nDetalle por región y categoría:")
    print(resumen_por_region(ventas).to_string(index=False))


if __name__ == "__main__":
    main()
