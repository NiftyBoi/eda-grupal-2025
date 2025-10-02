from src.eda import EDA

if __name__ == "__main__":
    eda = EDA("data/data.csv", sep=";", encoding="latin-1")
    eda.cargar_csv()
    eda.resumen_columnas()
    eda.descriptivos()

    # Análisis de fases
    resultados = eda.analizar_fases()

    # Histogramas y boxplots de numéricas
    eda.graficos_numericos()
