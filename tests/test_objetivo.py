from src.eda import EDA
from pathlib import Path

def test_analizar_fases(tmp_path: Path):
    eda = EDA("data/data.csv", sep=";", encoding="latin-1")
    eda.cargar_csv()
    resultados = eda.analizar_fases(save_path=tmp_path / "fases.png")

    # Debe devolver un diccionario con totales e IR
    assert "totales" in resultados
    assert "IR" in resultados

    # Los totales deben incluir F1, F2 y F3
    fases_df = resultados["totales"]
    for fase in ["F1", "F2", "F3"]:
        assert fase in fases_df.index

    # El gráfico debe haberse guardado
    assert (tmp_path / "fases.png").exists()
