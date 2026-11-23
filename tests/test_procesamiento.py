"""Pruebas unitarias del módulo ``src.procesamiento``.

Cada prueba compara el comportamiento observado contra un resultado esperado
conocido de antemano. Los datos se construyen dentro de la propia prueba para
que no dependa de archivos externos ni del orden de ejecución.

Casos cubiertos: normal, vacío e inválido.
"""

import pandas as pd
import pytest

from src.procesamiento import calcular_metricas_ventas, resumen_por_region


@pytest.fixture
def ventas_conocidas() -> pd.DataFrame:
    """Conjunto pequeño de transacciones con totales calculados a mano.

    Returns:
        pandas.DataFrame: Cuatro transacciones cuyas ventas suman 1000.00 y
            cuyas ganancias suman 150.00.
    """
    return pd.DataFrame(
        {
            "region": ["Centro", "Centro", "Occidente", "Oriente"],
            "categoria": ["Tecnologia", "Mobiliario", "Tecnologia", "Mobiliario"],
            "ventas": [100.00, 250.00, 400.00, 250.00],
            "ganancias": [30.00, 25.00, 80.00, 15.00],
        }
    )


@pytest.fixture
def ventas_vacias() -> pd.DataFrame:
    """DataFrame con la estructura correcta pero sin ninguna fila.

    Returns:
        pandas.DataFrame: Las cuatro columnas obligatorias, cero registros.
    """
    return pd.DataFrame(columns=["region", "categoria", "ventas", "ganancias"])


# --------------------------------------------------------------------------
# Caso normal
# --------------------------------------------------------------------------
def test_calculo_total_de_ventas(ventas_conocidas):
    """El total de ventas y de ganancias debe coincidir con la suma manual."""
    metricas = calcular_metricas_ventas(ventas_conocidas)

    assert metricas["total_ventas"] == 1000.00
    assert metricas["total_ganancias"] == 150.00
    assert metricas["num_transacciones"] == 4


def test_calculo_ticket_y_margen(ventas_conocidas):
    """El ticket promedio y el margen se derivan correctamente de los totales."""
    metricas = calcular_metricas_ventas(ventas_conocidas)

    assert metricas["ticket_promedio"] == 250.00  # 1000 / 4
    assert metricas["margen_porcentual"] == 15.00  # 150 / 1000 * 100


def test_filas_con_nulos_se_descartan():
    """Una fila con venta nula no debe alterar los totales ni el conteo."""
    con_nulo = pd.DataFrame(
        {
            "region": ["Centro", "Centro", "Occidente", "Oriente", "Centro"],
            "categoria": [
                "Tecnologia",
                "Mobiliario",
                "Tecnologia",
                "Mobiliario",
                "Tecnologia",
            ],
            "ventas": [100.00, 250.00, 400.00, 250.00, None],
            "ganancias": [30.00, 25.00, 80.00, 15.00, 10.00],
        }
    )

    metricas = calcular_metricas_ventas(con_nulo)

    assert metricas["num_transacciones"] == 4
    assert metricas["total_ventas"] == 1000.00


def test_resumen_por_region_agrupa_correctamente(ventas_conocidas):
    """El resumen debe producir una fila por combinación region-categoria."""
    resumen = resumen_por_region(ventas_conocidas)

    assert len(resumen) == 4
    fila = resumen[
        (resumen["region"] == "Centro") & (resumen["categoria"] == "Tecnologia")
    ].iloc[0]
    assert fila["total_ventas"] == 100.00
    assert fila["num_lineas"] == 1


# --------------------------------------------------------------------------
# Caso vacío
# --------------------------------------------------------------------------
def test_dataframe_vacio_devuelve_metricas_en_cero(ventas_vacias):
    """Sin registros la función responde con ceros, no con una excepción."""
    metricas = calcular_metricas_ventas(ventas_vacias)

    assert metricas["num_transacciones"] == 0
    assert metricas["total_ventas"] == 0.0
    assert metricas["total_ganancias"] == 0.0


def test_dataframe_vacio_no_divide_entre_cero(ventas_vacias):
    """Ticket promedio y margen valen 0.0 en lugar de producir NaN o ZeroDivisionError."""
    metricas = calcular_metricas_ventas(ventas_vacias)

    assert metricas["ticket_promedio"] == 0.0
    assert metricas["margen_porcentual"] == 0.0


def test_resumen_vacio_conserva_las_columnas(ventas_vacias):
    """El resumen de un DataFrame vacío mantiene el contrato de columnas."""
    resumen = resumen_por_region(ventas_vacias)

    assert resumen.empty
    assert list(resumen.columns) == [
        "region",
        "categoria",
        "num_lineas",
        "total_ventas",
        "total_ganancias",
    ]


# --------------------------------------------------------------------------
# Caso inválido
# --------------------------------------------------------------------------
def test_columna_faltante_levanta_value_error():
    """Si falta una columna obligatoria la función debe fallar de forma explícita."""
    incompleto = pd.DataFrame({"region": ["Centro"], "ventas": [100.00]})

    with pytest.raises(ValueError, match="Faltan columnas obligatorias"):
        calcular_metricas_ventas(incompleto)


def test_tipo_incorrecto_levanta_type_error():
    """Pasar algo que no es un DataFrame debe producir un TypeError claro."""
    with pytest.raises(TypeError):
        calcular_metricas_ventas([{"region": "Centro", "ventas": 100.00}])
