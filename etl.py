import pandas as pd

# Extraction [E]
def extract_from_csv(file, separator):
    df = pd.read_csv(file, sep=separator)
    return df

def extract_from_xls(file, name, usecols_name, skiprows_nb):
    df = pd.read_excel(
    file,
    sheet_name=name,
    usecols=usecols_name,
    skiprows=skiprows_nb
    )
    return df

def extract():
    # Extraction de puis les fichiers plats
    result_df = extract_from_csv("RawData/presidentielle-2022-resultat-departement.csv", ",")
    criminality_df = extract_from_csv("RawData/criminalite-par-departement.csv", ";")
    unemployment_df = extract_from_csv("RawData/chomage-par-departement-2022.csv", ",")
    imigration_df = extract_from_xls("RawData/imigration-departement.xlsx", "Figure 1", "B:C", 5)
    departments_df = extract_from_csv("RawData/donnees_departements.csv", ";")
    wealth_df = extract_from_xls("RawData/niveau-de-vie-annuel-departement.xlsx", "Données", "A,C", 3)
    population_df = extract_from_xls("RawData/estim-pop-dep-sexe-gca-1975-2023.xls", "2022", "A,C,D,E,F,G", 4)

    # Chamngement des noms de colonnes
    imigration_df.columns = ["code_departement", "pourcentage_immigration"]
    departments_df_filtered = departments_df[['DEP','NBCOM','PTOT']]
    departments_df_filtered.columns= ["code_departement", "nombre_communes", "nombres_habitants"]
    wealth_df.columns = ["code_departement", "niveau_de_vie_annuel_median"]
    population_df.columns = [
    "code_departement", "nombre_0-19ans", "nombre_20-39ans",
    "nombre_40-59ans", "nombre_60-74ans", "nombre_+75ans"
    ]

    # Fusion des différents dataframe en un
    merged_df_1 = pd.merge(result_df, criminality_df, on='code_departement', how='left')
    merged_df_2 = pd.merge(merged_df_1, unemployment_df[['code_departement', 'taux_chomage']], on='code_departement', how='left')
    merged_df_3 = pd.merge(merged_df_2, imigration_df, on='code_departement', how='left')
    merged_df_4 = pd.merge(merged_df_3, departments_df_filtered, on='code_departement', how='left')
    merged_df_5 = pd.merge(merged_df_4, wealth_df, on='code_departement', how='left')
    merged_df_6 = pd.merge(merged_df_5, population_df, on='code_departement', how='left')

    # Affichage de vérification
    print(merged_df_6.head(10))

    return merged_df_6


# Transformation [T]
def transform(df):
    # Filtre sur l'année 2022
    if "annee" in df.columns:
        year_filtered_df = df[df['annee'] == 2022].copy()
    else:
        year_filtered_df = df.copy()

    transformed_df = year_filtered_df[[
        "code_departement", "libelle_departement", "prenom", "nom",
        "voix", "taux_chomage", "pourcentage_immigration", "nombre_communes", "nombres_habitants", "niveau_de_vie_annuel_median", "nombre_0-19ans", "nombre_20-39ans", "nombre_40-59ans", "nombre_60-74ans", "nombre_+75ans", "indicateur", "taux_pour_mille"
    ]].copy()

    # Convertir les effectifs d'âge en pourcentages
    for age_col in [
        "nombre_0-19ans", "nombre_20-39ans", "nombre_40-59ans",
        "nombre_60-74ans", "nombre_+75ans"
    ]:
        transformed_df[f"pourcentage_{age_col}"] = (
            transformed_df[age_col] / transformed_df["nombres_habitants"]
        ) * 100

    transformed_df.drop(columns=[
        "nombre_0-19ans", "nombre_20-39ans", "nombre_40-59ans",
        "nombre_60-74ans", "nombre_+75ans"
    ], inplace=True)

    # Passage de ligne à colonne pour les incidents
    transformed_df["taux_pour_mille"] = transformed_df["taux_pour_mille"].astype(str).str.replace(",", ".").astype(float)

    pivot_df = transformed_df.pivot_table(
        index=[
            "code_departement", "libelle_departement", "prenom", "nom", "taux_chomage", "voix",
            "pourcentage_immigration", "nombre_communes", "nombres_habitants", "niveau_de_vie_annuel_median",
            "pourcentage_nombre_0-19ans", "pourcentage_nombre_20-39ans",
            "pourcentage_nombre_40-59ans", "pourcentage_nombre_60-74ans", "pourcentage_nombre_+75ans"
        ],
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


# [ETL Main]
extracted_df = extract()
transformed_df = transform(extracted_df)
load_df = load(transformed_df, "TransformedData/jdd.csv")

    