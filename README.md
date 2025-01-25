# Tableau de Bord Démographique Mondial

Ce projet présente un tableau de bord interactif pour visualiser et analyser les données démographiques mondiales, utilisant les données de la Banque Mondiale.

## Fonctionnalités

### Indicateurs Disponibles
- Population totale
- Taux de fécondité (enfants par femme)
- Taux de mortalité (décès/1000 habitants)
- Espérance de vie (années)
- Croissance de la population (% annuel)
- Population urbaine (% de la population totale)

### Visualisations
1. **Carte du Monde Interactive**
   - Visualisation des données par pays
   - Code couleur intuitif pour chaque indicateur
   - Informations détaillées au survol

2. **Évolution Temporelle**
   - Graphique de l'évolution mondiale depuis 1960
   - Affichage de la moyenne mondiale
   - Visualisation des valeurs minimales et maximales
   - Identification des pays aux extrêmes

3. **Top 10 Pays**
   - Classement des 10 premiers pays pour chaque indicateur
   - Mise à jour dynamique selon l'année sélectionnée
   - Visualisation en barres horizontales

4. **Évolution des Pays les Plus Peuplés**
   - Courbes d'évolution des 10 pays les plus peuplés
   - Données depuis 1960
   - Couleurs uniques pour chaque pays
   - Légende interactive

## Installation

1. Cloner le repository :
```bash
git clone [URL_DU_REPO]
```

2. Créer un environnement virtuel Python :
```bash
python -m venv .venv
```

3. Activer l'environnement virtuel :
```bash
# Windows
.venv\Scripts\activate
```

4. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## Utilisation

1. Lancer le dashboard :
```bash
python dashboard.py
```

2. Ouvrir un navigateur et accéder à :
```
http://127.0.0.1:8050
```

## Structure du Projet

- `collect_demographics.py` : Script pour collecter les données de la Banque Mondiale
- `dashboard.py` : Application Dash pour le tableau de bord
- `donnees_demographiques/` : Dossier contenant les données démographiques en CSV
- `requirements.txt` : Liste des dépendances Python

## Dépendances Principales

- Dash
- Plotly
- Pandas
- Requests

## Mise à Jour des Données

Les données sont collectées via l'API de la Banque Mondiale. Pour mettre à jour les données :

```bash
python collect_demographics.py
```

## Fonctionnalités Techniques

- Interface responsive avec Bootstrap
- Mise en cache des données pour de meilleures performances
- Gestion des erreurs et des données manquantes
- Traduction automatique des noms de pays en français
- Formatage intelligent des valeurs numériques
