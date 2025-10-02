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

    def crear_objetivo_desde_descripcion(self, target_col="OBJETIVO"):
        """Crea una columna binaria: CLIMA si la descripción contiene 'CLIMA', sino OTRO."""
        if self.df is None:
            raise ValueError("Primero carga el CSV con cargar_csv()")

        self.df[target_col] = self.df["DESCRIPCION"].apply(
            lambda x: "CLIMA" if "CLIMA" in str(x).upper() else "OTRO"
        )

        print(f"\nColumna '{target_col}' creada a partir de DESCRIPCION.")
        print(self.df[["DESCRIPCION", target_col]].head(10))
        return target_col

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

    def graficos_numericos(self, save_dir="outputs"):
        """Genera histogramas y boxplots para todas las columnas numéricas."""
        if self.df is None:
            raise ValueError("Primero carga el CSV con cargar_csv()")

        num_cols = self.df.select_dtypes(include=["int64", "float64"]).columns

        for col in num_cols:
            plt.figure()
            self.df[col].hist(bins=20)
            plt.title(f"Histograma de {col}")
            plt.xlabel(col)
            plt.ylabel("Frecuencia")
            plt.tight_layout()
            plt.savefig(f"{save_dir}/hist_{col}.png")
            plt.close()

            plt.figure()
            self.df.boxplot(column=col)
            plt.title(f"Boxplot de {col}")
            plt.tight_layout()
            plt.savefig(f"{save_dir}/box_{col}.png")
            plt.close()

        print(f"\nGráficos numéricos generados en {save_dir}/")

    def analizar_fases(self, save_path="outputs/distribucion_fases.png"):
        """
        Calcula la suma de WATTS por fase (F1, F2, F3) y evalúa el desbalance.
        """
        if self.df is None:
            raise ValueError("Primero carga el CSV con cargar_csv()")

        # Inicializar contadores
        fases = {"F1": 0, "F2": 0, "F3": 0}

        # Recorrer filas
        for _, row in self.df.iterrows():
            watts = row["WATTS"] if pd.notnull(row["WATTS"]) else 0
            if pd.notnull(row["F1"]) and str(row["F1"]).strip() != "":
                fases["F1"] += watts
            if pd.notnull(row["F2"]) and str(row["F2"]).strip() != "":
                fases["F2"] += watts
            if pd.notnull(row["F3"]) and str(row["F3"]).strip() != "":
                fases["F3"] += watts

        # Convertir a DataFrame para análisis
        fases_df = pd.DataFrame.from_dict(fases, orient="index", columns=["Total_WATTS"])

        # Calcular IR (desbalance entre mayor y menor carga)
        if fases_df["Total_WATTS"].min() > 0:
            ir = fases_df["Total_WATTS"].max() / fases_df["Total_WATTS"].min()
        else:
            ir = float("inf")

        print("\n⚡ Distribución de cargas por fase:")
        print(fases_df)
        print(f"Imbalance Ratio (IR) entre fases: {ir:.2f}")

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


