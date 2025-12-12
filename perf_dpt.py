import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats


# Load data
df = pd.read_csv('Extended_Employee_Performance_and_Productivity_Data.csv')



# Data Cleaning
viz = df.head()
desc = df.describe()
info = df.info()
col = df.columns
na = df.isna().sum()
natot = df.isna().sum().sum()

# Data vizualization

# Créer une grille de subplots (3 lignes, 2 colonnes)
fig, axes = plt.subplots(3, 2, figsize=(16, 14))

# Distribution des scores de performances
sns.histplot(df['Performance_Score'], bins=1, ax=axes[0, 0])
axes[0, 0].set_title('Distribution des scores de performances')
axes[0, 0].set_xlabel('score de performance')
axes[0, 0].set_ylabel('Nombre d\'employés')

# Distribution des scores de satisfaction des employés
sns.histplot(df['Employee_Satisfaction_Score'], bins=1, ax=axes[0, 1])
axes[0, 1].set_title('Distribution des scores de satisfaction des employés')
axes[0, 1].set_xlabel('score de satisfaction des employés')
axes[0, 1].set_ylabel('Nombre d\'employés')

# Boxplot des scores de performances par département
sns.boxplot(x=df['Department'], y=df['Performance_Score'], ax=axes[1, 0])
axes[1, 0].set_title('Score de performance par departement')
axes[1, 0].set_xlabel("Departement")
axes[1, 0].set_ylabel('Score de performance')
axes[1, 0].tick_params(axis='x', rotation=90)

# Boxplot des scores de satisfaction des employés par département
sns.boxplot(x=df['Department'], y=df['Employee_Satisfaction_Score'], ax=axes[1, 1])
axes[1, 1].set_title('Score de satisfaction des employés par departement')
axes[1, 1].set_xlabel("Departement")
axes[1, 1].set_ylabel('Score de satisfaction des employés')
axes[1, 1].tick_params(axis='x', rotation=90)

# Boxplot des scores de performances en fonction des heures travaillées par semaine
sns.boxplot(x=df['Work_Hours_Per_Week'], y=df['Performance_Score'], ax=axes[2, 0])
axes[2, 0].set_title('Score de performance en fonction des heures travaillées par semaine')
axes[2, 0].set_xlabel('Heures travaillées par semaine')
axes[2, 0].set_ylabel('Score de perfoemance')

# Masquer le dernier subplot vide
axes[2, 1].axis('off')

# Ajuster l'espacement
plt.tight_layout()

# Affichage de toutes les figures en même temps
plt.show()





# Occurrences de chaque valeur de Performance_Score 
print("\nComptage des scores de performance:")
print(df['Performance_Score'].value_counts().sort_index())

# Occurrences de chaque valeur de Employee_Satisfaction_Score
print("\nComptage des scores de satisfaction des employés:")
print(df['Employee_Satisfaction_Score'].value_counts().sort_index())

# Relation qualitative (indépendance entre satisfaction des employés et departement)
#Test du Chi2
# Hypothèses :
# H0 : Il n'y a pas de relation entre la satisfaction des employés et le département
# H1 : Il y a une relation entre la satisfaction des employés et le département

contingency_table = pd.crosstab(df['Department'], df['Employee_Satisfaction_Score'])
chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
if p_value < 0.05:
    print(f"\nTest du Chi2 entre satisfaction des employés et departement:\nChi2 = {chi2}, p-value = {p_value}\nRejet de H0 : Il y a une relation entre la satisfaction des employés et le département")
else:
    print(f"\nTest du Chi2 entre satisfaction des employés et departement:\nChi2 = {chi2}, p-value = {p_value}\nOn rejette pas H0 : Il n'y a pas de relation entre la satisfaction des employés et le département")

# V de Cramer
# Calcul du V de Cramer pour mesurer la force de l'association
n = contingency_table.sum().sum()
v_cramer = np.sqrt(chi2 / (n * (min(contingency_table.shape) - 1)))
if v_cramer <= 0.1:
    interpretation = "association négligeable"
elif v_cramer < 0.3:
    interpretation = "association faible"
elif v_cramer <= 0.5:
    interpretation = "association modérée"
elif v_cramer <= 0.8:
    interpretation = "association forte"
else:
    interpretation = "association très forte"
print(f"V de Cramer entre satisfaction des employés et departement: V = {v_cramer} ({interpretation})")   

# Test de normalité
# Test deShapiro-Wilk pour la normalité des scores de performance
shapiro_stat, shapiro_p = stats.shapiro(df['Performance_Score'])
if shapiro_p > 0.05:
    print(f"\nTest de Shapiro-Wilk pour la normalité des scores de performance:\nStatistique = {shapiro_stat}, p-value = {shapiro_p}\nLes données suivent une distribution normale")
else:
    print(f"\nTest de Shapiro-Wilk pour la normalité des scores de performance:\nStatistique = {shapiro_stat}, p-value = {shapiro_p}\nLes données ne suivent pas une distribution normale")

# Test d'homogénéité des variances
# Test deLevene pour l'homogénéité des variances des scores de performance
levene_stat, levene_p = stats.levene(*[df['Performance_Score'][df['Department'] == dept] for dept in df['Department'].unique()])
if levene_p > 0.05:
    print(f"\nTest de Levene pour l'homogénéité des variances des scores de performance:\nStatistique = {levene_stat}, p-value = {levene_p}\nLes variances sont homogènes entre les départements") 
else:
    print(f"\nTest de Levene pour l'homogénéité des variances des scores de performance:\nStatistique = {levene_stat}, p-value = {levene_p}\nLes variances ne sont pas homogènes entre les départements")


# Rélation qualitative quantitative (score de performance en fonction du département)
# Test Kruskal-Wallis
# Hypothèses :
# H0 : Les distributions des scores de performance sont identiques entre les départements
# H1 : Au moins une distribution des scores de performance est différente entre les départements

groups = [df['Performance_Score'][df['Department'] == dept] for dept in df['Department'].unique()]
kruskal_stat, kruskal_p = stats.kruskal(*groups)
if kruskal_p < 0.05:
    print(f"\nTest de Kruskal-Wallis pour les scores de performance entre les départements:\nStatistique = {kruskal_stat}, p-value = {kruskal_p}\nRejet de H0 : Au moins une distribution des scores de performance est différente entre les départements")
else:
    print(f"\nTest de Kruskal-Wallis pour les scores de performance entre les départements:\nStatistique = {kruskal_stat}, p-value = {kruskal_p}\nOn ne rejette pas H0 : Les distributions des scores de performance sont identiques entre les départements")

# Relation quantitative quantitative (score de performance en fonction du score de satisfaction des employés)
# Test de corrélation de Spearman
# Hypothèses : 
# H0 : Il n'y a pas de corrélation entre le score de performance et le score de satisfaction des employés
# H1 : Il y a une corrélation entre le score de performance et le score de satisfaction des employés
spearman_corr, spearman_p = stats.spearmanr(df['Performance_Score'], df['Employee_Satisfaction_Score'])
if spearman_p < 0.05:
    print(f"\nTest de corrélation de Spearman entre le score de performance et le score de satisfaction des employés:\nCoefficient de corrélation = {spearman_corr}, p-value = {spearman_p}\nRejet de H0 : Il y a une corrélation entre le score de performance et le score de satisfaction des employés")
else:
    print(f"\nTest de corrélation de Spearman entre le score de performance et le score de satisfaction des employés:\nCoefficient de corrélation = {spearman_corr}, p-value = {spearman_p}\nOn ne rejette pas H0 : Il n'y a pas de corrélation entre le score de performance et le score de satisfaction des employés")


# Relation quantitative quantitative (score de performance en fonction du nombre d'heures travaillées par semaine)
# Test de corrélation de Spearman
# Hypothèses :
# H0 : Il n'y a pas de corrélation entre le score de performance et le nombre d'heures travaillées par semaine
# H1 : Il y a une corrélation entre le score de performance et le nombre
spearman_corr_hours, spearman_p_hours = stats.spearmanr(df['Performance_Score'], df['Work_Hours_Per_Week'])
if spearman_p_hours < 0.05:
    print(f"\nTest de corrélation de Spearman entre le score de performance et le nombre d'heures travaillées par semaine:\nCoefficient de corrélation = {spearman_corr_hours}, p-value = {spearman_p_hours}\nRejet de H0 : Il y a une corrélation entre le score de performance et le nombre d'heures travaillées par semaine")
else:
    print(f"\nTest de corrélation de Spearman entre le score de performance et le nombre d'heures travaillées par semaine:\nCoefficient de corrélation = {spearman_corr_hours}, p-value = {spearman_p_hours}\nOn ne rejette pas H0 : Il n'y a pas de corrélation entre le score de performance et le nombre d'heures travaillées par semaine")