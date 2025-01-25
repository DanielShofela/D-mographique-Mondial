import requests
import json
from datetime import datetime
import os
import csv
import locale

def collect_demographic_data():
    # Configurer le format des nombres pour utiliser la virgule comme séparateur décimal
    locale.setlocale(locale.LC_NUMERIC, 'fr_FR.UTF-8')
    
    # Calculer la plage d'années (200 ans jusqu'à maintenant)
    current_year = datetime.now().year
    start_year = 1960
    
    # Indicateurs démographiques à collecter
    indicators = {
        'SP.POP.TOTL': {
            'name': 'population_totale',
            'description': 'Population totale',
            'unit': 'habitants'
        },
        'SP.DYN.TFRT.IN': {
            'name': 'taux_de_fécondité',
            'description': 'Taux de fécondité',
            'unit': 'enfants par femme'
        },
        'SP.DYN.CDRT.IN': {
            'name': 'taux_de_mortalité',
            'description': 'Taux de mortalité brut',
            'unit': 'décès/1000 habitants'
        },
        'SP.DYN.LE00.IN': {
            'name': 'espérance_de_vie',
            'description': 'Espérance de vie',
            'unit': 'années'
        },
        'SP.POP.GROW': {
            'name': 'croissance_de_la_population',
            'description': 'Croissance de la population',
            'unit': '%'
        },
        'SP.URB.TOTL.IN.ZS': {
            'name': 'population_urbaine_en_pourcentage',
            'description': 'Population urbaine',
            'unit': '%'
        },
    }
    
    # Créer le dossier de sortie s'il n'existe pas
    output_dir = 'donnees_demographiques'
    os.makedirs(output_dir, exist_ok=True)
    
    # URL de base de l'API de la Banque mondiale
    base_url = "http://api.worldbank.org/v2/countries/all/indicators"
    
    # Collecter les données pour chaque indicateur
    for indicator_code, indicator_info in indicators.items():
        print(f"Collecte des données pour : {indicator_info['description']}")
        
        # Préparer le fichier CSV
        if indicator_code == 'SP.URB.TOTL.IN.ZS':
            filename = f"{output_dir}/population_urbaine_en_pourcentage.csv"
        else:
            filename = f"{output_dir}/{indicator_info['name']}.csv"
        
        def save_data(data, filename, indicator_info):
            """Sauvegarde les données dans un fichier CSV."""
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Écrire l'en-tête avec les métadonnées
                writer.writerow(['# ' + indicator_info['description']])
                writer.writerow(['# Unité: ' + indicator_info['unit']])
                writer.writerow(['pays', 'code_pays', 'annee', 'valeur'])
                
                # Écrire les données
                for item in data:
                    if item.get('value') is not None:
                        writer.writerow([
                            item['country']['value'],
                            item['country']['id'],
                            item['date'],
                            item['value']  # Ne pas modifier le format des nombres
                        ])
        
        def get_data(indicator_code):
            """Récupère les données pour un indicateur donné."""
            all_data = []
            page = 1
            per_page = 1000
            
            while True:
                params = {
                    'format': 'json',
                    'per_page': per_page,
                    'page': page,
                    'date': f'{start_year}:{current_year}'  # Données disponibles depuis 1960
                }
                
                try:
                    print(f"Récupération de la page {page} pour {indicator_code}...")
                    response = requests.get(f"{base_url}/{indicator_code}", params=params)
                    response.raise_for_status()
                    data = response.json()
                    
                    # Vérifier si nous avons des données
                    if len(data) < 2 or not data[1]:
                        break
                    
                    # Ajouter les données de cette page
                    all_data.extend(data[1])
                    print(f"Reçu {len(data[1])} enregistrements")
                    
                    # Vérifier si c'est la dernière page
                    if len(data[1]) < per_page:
                        break
                    
                    page += 1
                    
                except Exception as e:
                    print(f"Erreur lors de la récupération des données pour {indicator_code}: {e}")
                    break
            
            print(f"Total des enregistrements collectés: {len(all_data)}")
            return all_data
        
        # Récupérer les données
        data = get_data(indicator_code)
        
        if data:
            # Sauvegarder les données
            save_data(data, filename, indicator_info)
            print(f"Données sauvegardées dans : {filename}")
            print(f"Nombre total d'enregistrements: {len(data)}")
            
            # Afficher la plage d'années couverte
            years = sorted(set(item['date'] for item in data))
            print(f"Période couverte: {min(years)} - {max(years)}")
        else:
            print(f"Aucune donnée trouvée pour {indicator_info['description']}")

if __name__ == "__main__":
    print("Début de la collecte des données démographiques mondiales...")
    collect_demographic_data()
    print("Collecte terminée!")
