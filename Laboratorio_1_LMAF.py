import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def generate_visualizations(analysis_results, df):
    """
    Genera visualizaciones para el análisis climático
    """
    plt.style.use('seaborn-v0_8')
    
    # 1. Tendencia temporal global
    if 'yearly_means' in analysis_results:
        plt.figure(figsize=(12, 6))
        analysis_results['yearly_means'].plot()
        plt.title('Evolución de la Temperatura Global (1961-2022)')
        plt.xlabel('Año')
        plt.ylabel('Temperatura (°C)')
        plt.grid(True)
        plt.show()
    
    # 2. Distribución de temperaturas
    year_columns = [col for col in df.columns if col.isdigit() and 1961 <= int(col) <= 2022]
    if year_columns:
        recent_year = max(year_columns, key=int)
        plt.figure(figsize=(10, 6))
        df[recent_year].hist(bins=30)
        plt.title(f'Distribución de Temperaturas ({recent_year})')
        plt.xlabel('Temperatura (°C)')
        plt.ylabel('Frecuencia')
        plt.show()
    
    # 3. Top 10 países más cálidos
    if year_columns:
        df['mean_temp'] = df[year_columns].mean(axis=1)
        top10_warmest = df.nlargest(10, 'mean_temp')[['country', 'mean_temp']]
        
        plt.figure(figsize=(12, 6))
        plt.barh(top10_warmest['country'], top10_warmest['mean_temp'])
        plt.title('Top 10 Países con Mayor Temperatura Media')
        plt.xlabel('Temperatura Media (°C)')
        plt.tight_layout()
        plt.show()

def create_final_report(analysis_results):
    """
    Crea un reporte final del análisis
    """
    print("\n" + "="*60)
    print("📋 REPORTE FINAL - ANÁLISIS DE CAMBIO CLIMÁTICO")
    print("="*60)
    
    if 'global_warming_trend' in analysis_results:
        trend = analysis_results['global_warming_trend']
        trend_text = "↗️ CALENTAMIENTO" if trend > 0 else "↘️ ENFRIAMIENTO" if trend < 0 else "➡️ ESTABLE"
        print(f"📈 Tendencia Global: {trend_text} ({trend:.4f}°C/año)")
    
    if 'yearly_means' in analysis_results:
        yearly_means = analysis_results['yearly_means']
        print(f"🌡️  Temperatura promedio 1961: {yearly_means.iloc[0]:.2f}°C")
        print(f"🌡️  Temperatura promedio 2022: {yearly_means.iloc[-1]:.2f}°C")
        change = yearly_means.iloc[-1] - yearly_means.iloc[0]
        print(f"📊 Cambio total: {change:+.2f}°C")
    
    print("="*60)
    