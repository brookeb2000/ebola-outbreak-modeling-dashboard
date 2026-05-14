# loading and cleaning data

import pandas as pd

def load_and_clean_ebola_data(
    file_path,
    country="Liberia",
    date_col="Date",
    country_col="Country",
    cases_col="Cumulative no. of confirmed, probable and suspected cases"
):
    """
    Load Ebola dataset, filter by country, clean daily cumulative case data,
    and add time column (t) as days since first reported case.

    Parameters:
        file_path (str): Path to CSV file
        country (str): Country to filter for
        date_col (str): Name of date column
        country_col (str): Name of country column
        cases_col (str): Name of cumulative cases column

    Returns:
        pd.DataFrame: Cleaned dataframe with Date, cumulative cases, and t
    """
    
    # Load data
    df = pd.read_csv(file_path)

    # Filter for selected country
    df_country = df[df[country_col] == country]

    # Keep one entry per day using max cumulative cases
    df_country = (
        df_country
        .groupby(date_col)[cases_col]
        .max()
        .reset_index()
    )

    # Convert Date column to datetime
    df_country[date_col] = pd.to_datetime(df_country[date_col])

    # Add time column (days since first reported case)
    df_country["t"] = (
        df_country[date_col] - df_country[date_col].min()
    ).dt.days

    return df_country