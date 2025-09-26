import pandas as pd

def load_data(path="dataset_climate_change.csv"):
    """Carga los datos del CSV y retorna lista de (país, iso3, valores)"""
    df = pd.read_csv(path)
    countries = []
    for _, row in df.iterrows():
        # Extraer valores de F1961 a F2022
        values = [row[f"F{year}"] for year in range(1961, 2023)]
        countries.append((row["Country"], row["ISO3"], values))
    return countries


def above_year_average(year, path="dataset_climate_change.csv"):
    """Promedio global de un año y países con valor > a ese promedio"""
    if year < 1961 or year > 2022:
        return None, []

    df = pd.read_csv(path)
    column = f"F{year}"

    # Calcular promedio del año (maneja NaN automáticamente)
    avg = df[column].mean(skipna=True)

    # Retornar promedio + lista de ISO3
    return avg, df[df[column] > avg]["ISO3"].tolist()


def below_global_average(year, path="dataset_climate_change.csv"):
    """Promedio global de todos los años y países con valor en ese año < ese promedio"""
    if year < 1961 or year > 2022:
        return None, []

    df = pd.read_csv(path)
    column = f"F{year}"

    # Calcular promedio global de todos los años (1961-2022)
    all_temp_columns = [f"F{y}" for y in range(1961, 2023)]
    global_avg = df[all_temp_columns].values.flatten()
    global_avg = pd.Series(global_avg).mean(skipna=True)

    # Retornar promedio global + lista de ISO3
    return global_avg, df[df[column] < global_avg]["ISO3"].tolist()


def above_mean(threshold, path="dataset_climate_change.csv"):
    """Países cuya media de temperatura >= threshold"""
    df = pd.read_csv(path)
    result = []

    temp_columns = [f"F{y}" for y in range(1961, 2023)]

    for _, row in df.iterrows():
        # Calcular media del país 
        country_mean = pd.Series([row[col] for col in temp_columns]).mean(skipna=True)
        if country_mean >= threshold:
            result.append(row["ISO3"])

    return result
