# 🗳️ Projet MSPR - Elexxion - Analyse et Prédiction de Tendances Électorales

Ce projet a été réalisé dans le cadre d'une **Mise en Situation Professionnelle Reconstituée (MSPR)**. Il consiste à concevoir une **preuve de concept (POC)** permettant d’analyser des données socio-économiques afin de **prédire les tendances électorales des élections présidentielles par département**.

---

## 📁 Structure du projet

```
📦 projet-mspr
├── RawData/              # Données brutes issues de l’INSEE, data.gouv.fr…
├── TransformedData/      # Données nettoyées et normalisées prêtes à être utilisées
├── etl.py                # Script Python contenant notre ETL
├── README.md            
```

---

## 🔄 ETL (etl.py)

Le fichier `etl.py` contient notre **pipeline de traitement de données** développé en **Python** à l’aide de la librairie **Pandas**. Il exécute les opérations suivantes :

- Chargement des fichiers bruts depuis le dossier `RawData/`
- Nettoyage et uniformisation des colonnes
- Gestion des valeurs manquantes
- Normalisation des unités et des formats
- Fusion des jeux de données par département
- Export du jeu de données final dans `TransformedData/`

Ce fichier prépare les données pour leur exploitation future : modélisation prédictive, visualisation, etc.

---

## 📚 Sources des données

- [INSEE](https://www.insee.fr)
- [data.gouv.fr](https://www.data.gouv.fr)

Les jeux de données incluent :
- Taux de chômage par département
- Taux de criminalité / incidents de sécurité
- Données démographiques et socio-économiques
- ...

---

## 🛠️ Lancer le projet

Téléchargement des dépendances
```
pip install pandas openpyxl xlrd
```

Lancement de l'ETL
```
python etl.py
```
---


