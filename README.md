# EDA Grupal ML

Proyecto desarrollado en el marco del diplomado en Machine Learning e Inteligencia Artificial.  
El objetivo es implementar un **Análisis Exploratorio de Datos (EDA)** mínimo y reproducible sobre un dataset en formato CSV, siguiendo buenas prácticas de **Python**, **POO** y **pruebas automáticas**.

## Objetivos del proyecto
- Cargar un CSV de forma robusta (ruta, separador y encoding).
- Analizar la calidad de las columnas: tipos de datos, valores faltantes, cardinalidad.
- Obtener descriptivos de variables numéricas y top categorías de variables categóricas.
- Explorar la distribución de la variable objetivo y calcular el **Imbalance Ratio (IR)**.
- Generar gráficos básicos: histogramas, boxplots y barras de la variable objetivo.
- Documentar hallazgos clave que afecten el preprocesamiento o el modelado posterior.

## Estructura del proyecto
```text
EDA_Grupal/
├── data/ # Dataset CSV
├── outputs/ # Gráficos y resultados del análisis
├── src/ # Código principal (clase EDA)
├── tests/ # Pruebas unitarias con pytest
├── main.py # Script para ejecutar el flujo completo
├── requirements.txt # Dependencias del proyecto
└── README.md # Este archivo
```
## Tecnologías utilizadas
- Python 3.10+  
- pandas  
- matplotlib  
- pytest  

## Cómo ejecutar
1. Clonar este repositorio:
``` bash
    git clone https://github.com/tuusuario/eda-grupal-ml.git
    cd eda-grupal-ml
```  
2. Crear entorno virtual e instalar dependencias:
```bash
    python -m venv venv
    .\venv\Scripts\activate   # Windows
    pip install -r requirements.txt
```

3. Colocar el dataset en la carpeta data/.

4. Ejecutar el análisis completo:
```bash
    python main.py
```
## Tests

Ejecuta los tests con:
```bash
    pytest -q
```
## Resultados

- Tabla de calidad de columnas (valores faltantes, tipos, cardinalidad).
- Descriptivos de numéricas y top categorías de texto.
- Distribución de la variable objetivo con gráfico y cálculo de IR.
- Gráficos en outputs/: histogramas, boxplots, barras de la variable objetivo.