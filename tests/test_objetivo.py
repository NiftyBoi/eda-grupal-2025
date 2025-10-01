from src.eda import EDA
from pathlib import Path

def test_analizar_objetivo(tmp_path: Path):
    eda = EDA("data/data.csv", sep=";", encoding="latin-1")
    eda.cargar_csv()
    resultados = eda.analizar_objetivo("EQUIPO CLIMA", save_path=tmp_path / "objetivo.png")

    # Debe devolver un diccionario con conteos, proporciones e IR
    assert "conteos" in resultados
    assert "proporciones" in resultados
    assert "IR" in resultados

    # El gráfico debe haberse guardado
    assert (tmp_path / "objetivo.png").exists()
