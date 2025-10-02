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
        """Carga el archivo CSV y muestra información básica."""
        if not self.file_path.exists():
            raise FileNotFoundError(f"No existe el archivo: {self.file_path}")

        self.df = pd.read_csv(self.file_path, sep=self.sep, encoding=self.encoding)

        print(f"\nArchivo cargado: {self.file_path}")
        print(f"Separador: {self.sep} | Encoding: {self.encoding}")
        print(f"Shape: {self.df.shape}")
        print("\nHead:\n", self.df.head())
        print("\nTipos de datos:\n", self.df.dtypes)

        return self.df

    def resumen_columnas(self):
        """Muestra resumen de tipos, nulos y cardinalidad."""
        if self.df is None:
            raise ValueError("Primero carga el CSV con cargar_csv()")

        resumen = pd.DataFrame({
            "dtype": self.df.dtypes,
            "n_missing": self.df.isnull().sum(),
            "pct_missing": self.df.isnull().mean() * 100,
            "n_unique": self.df.nunique()
        })
        # Columna adicional pedida en los tests
        resumen["maybe_binary_text"] = resumen["n_unique"].apply(lambda x: x == 2)

        print("\nResumen de columnas:")
        print(resumen)

        return resumen

    def descriptivos(self, top_n=10):
        """Muestra descriptivos numéricos y top categorías."""
        if self.df is None:
            raise ValueError("Primero carga el CSV con cargar_csv()")

        print("\nDescriptivos de variables numéricas:")
        print(self.df.describe().T)

        cat_cols = self.df.select_dtypes(include="object").columns
        resultados = {}
        print("\nTop categorías por columna categórica:")
        for col in cat_cols[:5]:
            top_cats = self.df[col].value_counts().head(top_n)
            print(f"\nColumna: {col}\n{top_cats}")
            resultados[col] = top_cats

        return resultados  # <- ahora sí devuelve dict

    def graficos_numericos(self, save_dir="outputs"):
        """Genera histogramas y boxplots de todas las columnas numéricas."""
        if self.df is None:
            raise ValueError("Primero carga el CSV con cargar_csv()")

        num_cols = self.df.select_dtypes(include=["int64", "float64"]).columns
        for col in num_cols:
            # Histograma
            plt.figure()
            self.df[col].hist(bins=20)
            plt.title(f"Histograma de {col}")
            plt.xlabel(col)
            plt.ylabel("Frecuencia")
            plt.tight_layout()
            plt.savefig(f"{save_dir}/hist_{col}.png")
            plt.close()

            # Boxplot
            plt.figure()
            self.df.boxplot(column=col)
            plt.title(f"Boxplot de {col}")
            plt.tight_layout()
            plt.savefig(f"{save_dir}/box_{col}.png")
            plt.close()

        print(f"\nGráficos numéricos guardados en {save_dir}/")

    def analizar_fases(self, save_path="outputs/distribucion_fases.png"):
        """Suma WATTS por fase (F1, F2, F3), evalúa desbalance y genera gráficos."""
        if self.df is None:
            raise ValueError("Primero carga el CSV con cargar_csv()")

        fases = {"F1": 0, "F2": 0, "F3": 0}
        for _, row in self.df.iterrows():
            watts = row["WATTS"] if pd.notnull(row["WATTS"]) else 0
            if pd.notnull(row["F1"]) and str(row["F1"]).strip() != "":
                fases["F1"] += watts
            if pd.notnull(row["F2"]) and str(row["F2"]).strip() != "":
                fases["F2"] += watts
            if pd.notnull(row["F3"]) and str(row["F3"]).strip() != "":
                fases["F3"] += watts

        fases_df = pd.DataFrame.from_dict(fases, orient="index", columns=["Total_WATTS"])
        ir = fases_df["Total_WATTS"].max() / fases_df["Total_WATTS"].min() if fases_df["Total_WATTS"].min() > 0 else float("inf")

        print("\nDistribución de cargas por fase:")
        print(fases_df)
        print(f"Imbalance Ratio (IR): {ir:.2f}")

        # Gráfico de barras
        fases_df.plot(kind="bar", legend=False, title="Distribución de WATTS por fase")
        plt.ylabel("Total WATTS")
        plt.tight_layout()
        plt.savefig(save_path)
        plt.close()

        # Pie chart
        plt.figure()
        fases_df["Total_WATTS"].plot(
            kind="pie",
            autopct="%1.1f%%",
            startangle=90,
            colormap="viridis",
            ylabel=""
        )
        plt.title("Proporción de carga por fase")
        plt.tight_layout()
        plt.savefig("outputs/distribucion_fases_pie.png")
        plt.close()

        return {"totales": fases_df, "IR": ir}
