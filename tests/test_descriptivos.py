from src.eda import EDA

def test_descriptivos_y_top_categorias():
    eda = EDA("data/data.csv", sep=";", encoding="latin-1")
    eda.cargar_csv()
    resultados = eda.descriptivos(top_n=5)

    assert isinstance(resultados, dict)

    # Si existe al menos una columna categórica, su top debe ser una serie
    if resultados:
        for col, serie in resultados.items():
            assert hasattr(serie, "head")  # es un objeto tipo Series
            assert serie.shape[0] <= 5     # top_n=5
