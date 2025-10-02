from src.eda import EDA

if __name__ == "__main__":
    try:
        eda = EDA("data/data.csv", sep=";", encoding="latin-1")
        eda.cargar_csv()
        eda.resumen_columnas()
        eda.descriptivos()

        # Análisis de fases
        resultados = eda.analizar_fases()

        # Histogramas y boxplots de numéricas
        eda.graficos_numericos()

        print("\nEjecución finalizada correctamente.")

    except Exception as e:
        print(f"\nError en la ejecución del análisis: {e}")
