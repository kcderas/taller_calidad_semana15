"""Procesamiento y cálculo de métricas de ventas.

Este módulo concentra la lógica de negocio del taller: recibe un conjunto de
transacciones de venta y devuelve las métricas agregadas que consume la capa
de presentación (reportes, notebooks o una futura API).

El módulo no lee archivos ni se conecta a ninguna base de datos. Recibe un
``DataFrame`` ya construido y devuelve estructuras de Python simples, de modo
que pueda verificarse de forma aislada con pruebas unitarias.

Columnas esperadas en el ``DataFrame`` de entrada:
    region (str), categoria (str), ventas (float), ganancias (float).
"""

from __future__ import annotations

import pandas as pd

COLUMNAS_REQUERIDAS = ("region", "categoria", "ventas", "ganancias")


def validar_estructura(dataframe: pd.DataFrame) -> None:
    """Comprueba que el DataFrame tenga las columnas que el módulo necesita.

    Args:
        dataframe (pandas.DataFrame): Conjunto de transacciones a validar.

    Returns:
        None: La función no devuelve valor; su efecto es levantar una
            excepción cuando la estructura no es la esperada.

    Raises:
        TypeError: Si el argumento no es un ``pandas.DataFrame``.
        ValueError: Si falta alguna de las columnas de
            :data:`COLUMNAS_REQUERIDAS`.
    """
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError(
            f"Se esperaba un pandas.DataFrame y se recibió {type(dataframe).__name__}"
        )

    faltantes = [c for c in COLUMNAS_REQUERIDAS if c not in dataframe.columns]
    if faltantes:
        raise ValueError(
            "Faltan columnas obligatorias: "
            f"{', '.join(faltantes)}. Columnas recibidas: {list(dataframe.columns)}"
        )


def calcular_metricas_ventas(dataframe: pd.DataFrame) -> dict:
    """Calcula las métricas globales de un conjunto de transacciones de venta.

    La función descarta las filas con valores nulos en las columnas numéricas
    antes de agregar, de modo que un registro incompleto no contamine los
    totales. Un ``DataFrame`` sin registros se considera una entrada válida y
    produce métricas en cero, no un error: permite que un reporte se genere
    aunque el período consultado no tenga movimientos.

    Args:
        dataframe (pandas.DataFrame): Transacciones de venta. Debe contener
            las columnas ``region`` (str), ``categoria`` (str),
            ``ventas`` (float) y ``ganancias`` (float).

    Returns:
        dict: Métricas agregadas con las siguientes claves:
            - ``num_transacciones`` (int): Cantidad de registros válidos.
            - ``total_ventas`` (float): Suma de la columna ``ventas``,
              redondeada a dos decimales.
            - ``total_ganancias`` (float): Suma de la columna ``ganancias``,
              redondeada a dos decimales.
            - ``ticket_promedio`` (float): Venta promedio por transacción.
              Vale ``0.0`` cuando no hay registros.
            - ``margen_porcentual`` (float): Ganancias sobre ventas,
              expresado en porcentaje. Vale ``0.0`` cuando el total de ventas
              es cero, para evitar una división indefinida.

    Raises:
        TypeError: Si ``dataframe`` no es un ``pandas.DataFrame``.
        ValueError: Si falta alguna de las columnas obligatorias.

    Examples:
        >>> import pandas as pd
        >>> datos = pd.DataFrame({
        ...     "region": ["Centro", "Occidente"],
        ...     "categoria": ["Tecnologia", "Mobiliario"],
        ...     "ventas": [100.0, 300.0],
        ...     "ganancias": [20.0, 30.0],
        ... })
        >>> metricas = calcular_metricas_ventas(datos)
        >>> metricas["total_ventas"]
        400.0
        >>> metricas["ticket_promedio"]
        200.0
    """
    validar_estructura(dataframe)

    datos = dataframe.dropna(subset=["ventas", "ganancias"])

    num_transacciones = int(len(datos))
    total_ventas = float(datos["ventas"].sum())
    total_ganancias = float(datos["ganancias"].sum())

    ticket_promedio = total_ventas / num_transacciones if num_transacciones else 0.0
    margen_porcentual = (total_ganancias / total_ventas * 100) if total_ventas else 0.0

    return {
        "num_transacciones": num_transacciones,
        "total_ventas": round(total_ventas, 2),
        "total_ganancias": round(total_ganancias, 2),
        "ticket_promedio": round(ticket_promedio, 2),
        "margen_porcentual": round(margen_porcentual, 2),
    }


def resumen_por_region(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Agrupa las transacciones por región y categoría.

    Complementa a :func:`calcular_metricas_ventas` cuando se necesita el
    detalle y no solo el consolidado.

    Args:
        dataframe (pandas.DataFrame): Transacciones de venta con las mismas
            columnas que exige :func:`calcular_metricas_ventas`.

    Returns:
        pandas.DataFrame: Una fila por combinación de región y categoría, con
            las columnas ``region``, ``categoria``, ``num_lineas``,
            ``total_ventas`` y ``total_ganancias``, ordenadas por región y
            categoría. Si la entrada no tiene registros, devuelve un
            ``DataFrame`` vacío con esas mismas columnas.

    Raises:
        TypeError: Si ``dataframe`` no es un ``pandas.DataFrame``.
        ValueError: Si falta alguna de las columnas obligatorias.
    """
    validar_estructura(dataframe)

    columnas_salida = [
        "region",
        "categoria",
        "num_lineas",
        "total_ventas",
        "total_ganancias",
    ]

    datos = dataframe.dropna(subset=["ventas", "ganancias"])
    if datos.empty:
        return pd.DataFrame(columns=columnas_salida)

    resumen = (
        datos.groupby(["region", "categoria"], as_index=False)
        .agg(
            num_lineas=("ventas", "size"),
            total_ventas=("ventas", "sum"),
            total_ganancias=("ganancias", "sum"),
        )
        .sort_values(["region", "categoria"])
        .reset_index(drop=True)
    )
    resumen["total_ventas"] = resumen["total_ventas"].round(2)
    resumen["total_ganancias"] = resumen["total_ganancias"].round(2)

    return resumen[columnas_salida]
