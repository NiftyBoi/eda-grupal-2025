from src.eda import EDA

def test_carga_csv_ok():
    eda = EDA("data/data.csv", sep=";", encoding="latin-1")
    df = eda.cargar_csv()

    # El dataframe no debería estar vacío
    assert not df.empty

    # Columnas esperadas según el nuevo CSV
    expected_cols = ["Tablero", "Ubicación", "DESCRIPCION", "WATTS", "F1", "F2", "F3", "mm2", "P_A", "mA", "AMP", "N CTO"]
    assert list(df.columns) == expected_cols

    # Verificamos que no aparezcan símbolos raros en la columna de descripción
    assert not any("�" in str(x) for x in df["DESCRIPCION"])

def test_resumen_columnas():
    eda = EDA("data/data.csv", sep=";", encoding="latin-1")
    eda.cargar_csv()
    resumen = eda.resumen_columnas()

    # Debe tener tantas filas como columnas hay en el dataset
    assert resumen.shape[0] == eda.df.shape[1]

    # Debe contener las columnas correctas en el resumen
    for col in ["dtype", "n_missing", "pct_missing", "n_unique", "maybe_binary_text"]:
        assert col in resumen.columns
