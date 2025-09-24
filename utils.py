import pandas as pd

def load_data(path="dataset_climate_change.csv"):
    """Carga los datos del CSV y retorna lista de (país, iso3, valores)"""
    df = pd.read_csv(path)
    countries = []
    for _, row in df.iterrows():
        # Extraer valores de F1961 a F2022 (62 años)
        values = [row[f"F{year}"] for year in range(1961, 2023)]
        countries.append((row["Country"], row["ISO3"], values))
    return countries

def above_year_average(year, path="dataset_climate_change.csv"):
    """Países con temperatura en un año > promedio de todos los países en ese año"""
    if year < 1961 or year > 2022:
        return []
    
    df = pd.read_csv(path)
    column = f"F{year}"
    
    # Calcular promedio del año (excluyendo NaN)
    avg = df[column].mean()
    
    # Retornar países que superan el promedio
    return df[df[column] > avg]["ISO3"].tolist()

def below_global_average(year, path="dataset_climate_change.csv"):
    """Países con temperatura en un año < promedio global de todos los años"""
    if year < 1961 or year > 2022:
        return []
    
    df = pd.read_csv(path)
    column = f"F{year}"
    
    # Calcular promedio global de todos los años (1961-2022)
    all_temp_columns = [f"F{y}" for y in range(1961, 2023)]
    global_avg = df[all_temp_columns].values.flatten()
    global_avg = pd.Series(global_avg).mean()  # Maneja NaN automáticamente
    
    # Retornar países con temperatura en ese año menor al promedio global
    return df[df[column] < global_avg]["ISO3"].tolist()

def above_mean(threshold, path="dataset_climate_change.csv"):
    """Países cuya media de temperatura >= threshold"""
    df = pd.read_csv(path)
    result = []
    
    for _, row in df.iterrows():
        # Calcular media del país para todos los años
        temp_columns = [f"F{y}" for y in range(1961, 2023)]
        country_values = [row[col] for col in temp_columns]
        country_mean = sum(country_values) / len(country_values)
        
        if country_mean >= threshold:
            result.append(row["ISO3"])
    
    return result