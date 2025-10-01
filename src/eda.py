import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

class EDA:
    def __init__(self, file_path, sep=";", encoding="latin-1"):
        self.file_path = Path(file_path)
        self.sep = sep
        self.encoding = encoding
        self.df = None

    def cargar_csv(self):
        if not self.file_path.exists():
            raise FileNotFoundError(f"No existe el archivo: {self.file_path}")

        # carga robusta
        self.df = pd.read_csv(self.file_path, sep=self.sep, encoding=self.encoding)

        # evidencia que pide la rúbrica
        print(f"Archivo: {self.file_path}")
        print(f"Separador: {self.sep}, Encoding: {self.encoding}")
        print(f"Shape: {self.df.shape}")
        print("\nhead():")
        print(self.df.head())
        print("\ndtypes:")
        print(self.df.dtypes)

        return self.df

    def resumen_columnas(self):
        if self.df is None:
            raise ValueError("Primero carga el CSV con cargar_csv()")

        resumen = pd.DataFrame({
            "dtype": self.df.dtypes,
            "n_missing": self.df.isnull().sum(),
            "pct_missing": self.df.isnull().mean() * 100,
            "n_unique": self.df.nunique()
        })

        resumen["maybe_binary_text"] = resumen["n_unique"].apply(lambda x: x == 2)
        resumen = resumen.sort_values(["pct_missing", "n_unique"], ascending=[False, True])

        print("\nResumen de calidad de columnas:")
        print(resumen.head(10))

        return resumen
    
    def descriptivos(self, top_n=10):
        if self.df is None:
            raise ValueError("Primero carga el CSV con cargar_csv()")

        print("\nDescriptivos de variables numéricas:")
        print(self.df.describe().T)

        # Identificar columnas categóricas
        cat_cols = self.df.select_dtypes(include="object").columns

        print("\nTop categorías por columna categórica:")
        resultados = {}
        for col in cat_cols[:5]:  # máximo 5 columnas representativas
            top_cats = self.df[col].value_counts().head(top_n)
            print(f"\nColumna: {col}")
            print(top_cats)
            resultados[col] = top_cats

        return resultados

    def analizar_objetivo(self, target_col, save_path="outputs/distribucion_objetivo.png"):
        if self.df is None:
            raise ValueError("Primero carga el CSV con cargar_csv()")

        if target_col not in self.df.columns:
            raise ValueError(f"La columna objetivo '{target_col}' no existe en el dataset")

        conteos = self.df[target_col].value_counts()
        proporciones = self.df[target_col].value_counts(normalize=True)
        ir = conteos.max() / conteos.min()

        print(f"\nVariable objetivo: {target_col}")
        print("Conteos:\n", conteos)
        print("Proporciones:\n", proporciones)
        print(f"Imbalance Ratio (IR): {ir:.2f}")

        # gráfico de barras
        conteos.plot(kind="bar", title=f"Distribución de {target_col}")
        plt.xlabel(target_col)
        plt.ylabel("Frecuencia")
        plt.tight_layout()
        plt.savefig(save_path)
        plt.close()

        return {"conteos": conteos, "proporciones": proporciones, "IR": ir}