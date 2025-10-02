from src.eda import EDA

def test_agregar_columna_fase():
    eda = EDA("data/data.csv", sep=";", encoding="latin-1")
    eda.cargar_csv()

    # Ejecutamos el método que crea la columna
    col = eda.agregar_columna_fase()

    # Verificamos que la columna se haya creado en el DataFrame
    assert "FASE_ASIGNADA" in eda.df.columns

    # La serie devuelta debe tener la misma longitud que el dataframe
    assert len(col) == len(eda.df)

    # Los valores deben ser solamente F1, F2, F3 o NINGUNA
    valores_unicos = set(col.unique())
    assert valores_unicos.issubset({"F1", "F2", "F3", "NINGUNA"})

    # Debe existir al menos un valor válido distinto de NINGUNA
    assert any(val in {"F1", "F2", "F3"} for val in valores_unicos)
