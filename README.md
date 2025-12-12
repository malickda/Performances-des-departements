# 📊 Analyse de la Performance et de la Satisfaction des Employés

## 📝 Description du Projet
Ce projet vise à analyser les facteurs potentiels influençant la performance des employés au sein d'une entreprise fictive. L'objectif principal est d'explorer les relations entre des variables **qualitatives** (Département, Satisfaction) et **quantitatives** (Score de performance, Heures travaillées) pour identifier des leviers d'amélioration.

L'analyse repose sur un jeu de données de **100 000 entrées**.

## 📂 Structure du Jeu de Données
Le fichier source : `Extended_Employee_Performance_and_Productivity_Data.csv`

Il contient **20 colonnes** sans valeurs manquantes. Les variables clés étudiées sont :
* **Qualitatives :** `Department` (IT, Sales, HR...), `Gender`, `Job_Title`.
* **Quantitatives :**
    * `Performance_Score` (Variable cible, note de 1 à 5).
    * `Employee_Satisfaction_Score` (Score de 1 à 5).
    * `Work_Hours_Per_Week` (Heures travaillées par semaine).

## 🛠️ Prérequis et Installation

### Environnement
* Python 3.x

### Bibliothèques nécessaires
Le projet utilise les bibliothèques standards de Data Science :
```bash
pip install pandas numpy matplotlib seaborn scipy
