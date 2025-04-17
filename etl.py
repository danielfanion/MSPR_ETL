import pandas as pd

# Extraction [E]
def extract_from_csv(file, separator):
    df = pd.read_csv(file, sep=separator)
    return df

def extract():
    result_df = extract_from_csv("RawData/presidentielle-2022-resultat-departement.csv", ",")
    criminality_df = extract_from_csv("RawData/criminalite-par-departement.csv", ";")

    print("Colonnes result_df :", result_df.columns.tolist())
    print("Colonnes criminality_df :", criminality_df.columns.tolist())

    merged_df = pd.merge(result_df, criminality_df, on='code_departement', how='left')

    return merged_df

# Transformation [T]
def transform(df):
    transformed_df = df[["code_departement", "libelle_departement", "prenom", "nom", "voix", "indicateur","taux_pour_mille"]]

    transformed_df["taux_pour_mille"] = df["taux_pour_mille"].str.replace(",", ".").astype(float)

    # On cherche à passer les lignes "indicateur" en colonne
    pivot_df = transformed_df.pivot_table(
        index=["code_departement", "libelle_departement", "prenom", "nom"],
        columns="indicateur",
        values="taux_pour_mille"
    )

    pivot_df.columns = [f"taux_pour_mille_{col}" for col in pivot_df.columns]
    pivot_df = pivot_df.reset_index()

    return pivot_df

# Chargement [L]
def load(data_to_load, target_file):
    data_to_load.to_csv(target_file)


# [ETL]
extracted_df = extract()
transformed_df = transform(extracted_df)
load_df = load(transformed_df, "TransformedData/jdd.csv")

    