from src.eda import EDA

if __name__ == "__main__":
    # 1. Crear objeto EDA con tu CSV
    eda = EDA("data/data.csv", sep=";", encoding="latin-1")

    # 2. Cargar el CSV
    df = eda.cargar_csv()

    # 3. Resumen de calidad de columnas
    resumen = eda.resumen_columnas()

    # 4. Descriptivos y top-categorías
    resultados = eda.descriptivos(top_n=10)

    # 5. Analizar la variable objetivo (ejemplo: EQUIPO CLIMA)
    analisis_obj = eda.analizar_objetivo("EQUIPO CLIMA")

    # Mostrar todo el resumen (no solo head)
    print("\nResumen completo de columnas:")
