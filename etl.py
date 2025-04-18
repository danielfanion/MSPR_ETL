import pandas as pd

# Extraction [E]
def extract_from_csv(file, separator):
    df = pd.read_csv(file, sep=separator)
    return df

def extract():
    result_df = extract_from_csv("RawData/presidentielle-2022-resultat-departement.csv", ",")
    criminality_df = extract_from_csv("RawData/criminalite-par-departement.csv", ";")
    unemployment_df = extract_from_csv("RawData/chomage-par-departement-2022.csv", ",")

    merged_df_1 = pd.merge(result_df, criminality_df, on='code_departement', how='left')
    merged_df = pd.merge(merged_df_1, unemployment_df[['code_departement', 'taux_chomage']], on='code_departement', how='left')

    print(merged_df[['code_departement', 'libelle_departement', 'taux_chomage']].head(10))

    return merged_df


# Transformation [T]
def transform(df):
    year_filtered_df = df[df['annee'] == 2022]

    transformed_df = year_filtered_df[[
        "code_departement", "libelle_departement", "prenom", "nom",
        "voix", "taux_chomage", "indicateur", "taux_pour_mille"
    ]].copy()

    transformed_df["taux_pour_mille"] = transformed_df["taux_pour_mille"].str.replace(",", ".").astype(float)

    pivot_df = transformed_df.pivot_table(
        index=["code_departement", "libelle_departement", "prenom", "nom", "taux_chomage", "voix"],
        columns="indicateur",
        values="taux_pour_mille"
    ).reset_index()

    pivot_df.columns = [
        col if isinstance(col, str) else f"taux_pour_mille_{col}"
        for col in pivot_df.columns
    ]

    return pivot_df


# Chargement [L]
def load(data_to_load, target_file):
    data_to_load.to_csv(target_file)


# [ETL]
extracted_df = extract()
transformed_df = transform(extracted_df)
load_df = load(transformed_df, "TransformedData/jdd.csv")

    