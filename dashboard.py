import os
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import datetime

# Dictionnaire pour stocker les correspondances entre noms d'affichage et noms de fichiers
INDICATOR_MAPPING = {}

# Configuration des indicateurs
INDICATORS = {
    'population_totale': {
        'display': 'Population totale',
        'unit': 'habitants',
        'format': '.0f'
    },
    'taux_de_fécondité': {
        'display': 'Taux de fécondité',
        'unit': 'enfants par femme',
        'format': '.1f'
    },
    'taux_de_mortalité': {
        'display': 'Taux de mortalité',
        'unit': 'décès/1000 habitants',
        'format': '.1f'
    },
    'espérance_de_vie': {
        'display': 'Espérance de vie',
        'unit': 'années',
        'format': '.1f'
    },
    'croissance_de_la_population': {
        'display': 'Croissance de la population',
        'unit': '% annuel',
        'format': '.1f'
    },
    'population_urbaine_en_pourcentage': {
        'display': 'Population urbaine',
        'unit': '% de la population totale',
        'format': '.1f'
    }
}

# Définir les unités pour chaque indicateur
UNITS = {
    'population_totale': 'habitants',
    'taux_de_fécondité': 'enfants par femme',
    'taux_de_mortalité': 'décès/1000 habitants',
    'espérance_de_vie': 'années',
    'croissance_de_la_population': '% annuel',
    'population_urbaine_en_pourcentage': '% de la population totale'
}

# Définir les échelles de couleurs pour chaque indicateur
COLOR_SCALES = {
    'population_totale': 'Blues',
    'taux_de_fécondité': 'Viridis',
    'taux_de_mortalité': 'Reds',
    'espérance_de_vie': 'RdYlGn',
    'croissance_de_la_population': 'RdYlBu',
    'population_urbaine_en_pourcentage': 'Purples'
}

# Définir une palette de couleurs distinctes pour les 10 pays
COUNTRY_COLORS = {
    'Chine': '#1f77b4',  # Bleu
    'Inde': '#ff7f0e',  # Orange
    'États-Unis': '#2ca02c',  # Vert
    'Indonésie': '#d62728',  # Rouge
    'Pakistan': '#9467bd',  # Violet
    'Brésil': '#8c564b',  # Marron
    'Nigéria': '#e377c2',  # Rose
    'Bangladesh': '#7f7f7f',  # Gris
    'Russie': '#bcbd22',  # Jaune-vert
    'Mexique': '#17becf'   # Cyan
}

# Mapping des noms de pays anglais vers français
COUNTRY_NAMES = {
    'China': 'Chine',
    'India': 'Inde',
    'United States': 'États-Unis',
    'Indonesia': 'Indonésie',
    'Pakistan': 'Pakistan',
    'Brazil': 'Brésil',
    'Nigeria': 'Nigéria',
    'Bangladesh': 'Bangladesh',
    'Russian Federation': 'Russie',
    'Mexico': 'Mexique'
}

# Liste des vrais pays
REAL_COUNTRIES = {
    'China': 'Chine',
    'India': 'Inde',
    'Indonesia': 'Indonésie',
    'Pakistan': 'Pakistan',
    'Brazil': 'Brésil',
    'Nigeria': 'Nigéria',
    'Bangladesh': 'Bangladesh',
    'Russian Federation': 'Russie',
    'Mexico': 'Mexique',
    'Japan': 'Japon',
    'Ethiopia': 'Éthiopie',
    'Philippines': 'Philippines',
    'Egypt, Arab Rep.': 'Égypte',
    'Vietnam': 'Vietnam',
    'Congo, Dem. Rep.': 'République démocratique du Congo',
    'Turkey': 'Turquie',
    'Iran, Islamic Rep.': 'Iran',
    'Germany': 'Allemagne',
    'Thailand': 'Thaïlande',
    'United Kingdom': 'Royaume-Uni',
    'France': 'France',
    'Italy': 'Italie',
    'South Africa': 'Afrique du Sud',
    'Myanmar': 'Myanmar',
    'Kenya': 'Kenya',
    'Colombia': 'Colombie',
    'Spain': 'Espagne',
    'Uganda': 'Ouganda',
    'Argentina': 'Argentine',
    'Algeria': 'Algérie',
    'Sudan': 'Soudan',
    'Ukraine': 'Ukraine',
    'Iraq': 'Irak',
    'Afghanistan': 'Afghanistan',
    'Poland': 'Pologne',
    'Canada': 'Canada',
    'Morocco': 'Maroc',
    'Saudi Arabia': 'Arabie Saoudite',
    'Uzbekistan': 'Ouzbékistan',
    'Peru': 'Pérou',
    'Malaysia': 'Malaisie'
}

def translate_country_name(name):
    """Traduit le nom du pays de l'anglais vers le français"""
    return COUNTRY_NAMES.get(name, name)

# Fonction pour obtenir un nom d'affichage plus lisible
def get_display_name(filename):
    """Convertit un nom de fichier en nom d'affichage."""
    # Enlever l'extension .csv
    name = filename.replace('.csv', '')
    # Remplacer les underscores par des espaces
    name = name.replace('_', ' ')
    # Mettre en majuscule la première lettre de chaque mot
    return name.title()

def get_file_name(display_name):
    """Convertit un nom d'affichage en nom de fichier."""
    return INDICATOR_MAPPING.get(display_name, '')

def load_data(indicator):
    """Charge les données pour un indicateur donné."""
    filename = os.path.join('donnees_demographiques', f"{indicator}.csv")
    
    try:
        # Ignorer les lignes qui commencent par #
        df = pd.read_csv(filename, comment='#')
        
        # Renommer les colonnes si nécessaire
        df.columns = ['pays', 'code_pays', 'annee', 'valeur']
        
        # Convertir l'année en entier
        df['annee'] = pd.to_numeric(df['annee'], errors='coerce').astype('Int64')
        
        # Convertir la valeur en float
        df['valeur'] = pd.to_numeric(df['valeur'], errors='coerce')
        
        return df
    except Exception as e:
        print(f"Erreur lors du chargement de {filename}: {e}")
        return pd.DataFrame(columns=['pays', 'code_pays', 'annee', 'valeur'])

def create_top10_evolution(df):
    """Créer le graphique d'évolution des 10 pays les plus peuplés actuellement"""
    # Obtenir l'année la plus récente
    latest_year = df['annee'].max()
    
    # Filtrer pour ne garder que les vrais pays
    df_latest = df[df['annee'] == latest_year].copy()
    df_latest = df_latest[df_latest['pays'].isin(REAL_COUNTRIES.keys())]
    
    # Obtenir les 10 pays les plus peuplés
    top10_countries = df_latest.nlargest(10, 'valeur')['pays'].tolist()
    
    # Filtrer les données pour ces 10 pays sur toute la période
    df_top10 = df[df['pays'].isin(top10_countries)]
    
    # Créer le graphique
    fig = go.Figure()
    
    for country in top10_countries:
        country_data = df_top10[df_top10['pays'] == country]
        country_name_fr = REAL_COUNTRIES[country]
        
        fig.add_trace(
            go.Scatter(
                x=country_data['annee'],
                y=country_data['valeur'],
                name=country_name_fr,
                line=dict(
                    color=COUNTRY_COLORS.get(country_name_fr, '#000000'),
                    width=2
                ),
                hovertemplate="%{x}<br>" +
                             f"{country_name_fr}: " +
                             "%{y:,.0f} habitants<br>" +
                             "<extra></extra>"
            )
        )
    
    fig.update_layout(
        title="Évolution de la population des 10 pays les plus peuplés",
        xaxis_title="Année",
        yaxis_title="Population",
        hovermode='x unified',
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.05
        ),
        margin=dict(r=150)  # Marge à droite pour la légende
    )
    
    # Formater l'axe Y pour utiliser des milliards/millions
    fig.update_yaxes(
        tickformat=".2s",
        hoverformat=",d"
    )
    
    return fig

# Charger les données
print("\nChargement des données...")
data_dir = 'donnees_demographiques'
datasets = {}

# Créer le mapping des indicateurs et charger les données
print("\nCréation du mapping des indicateurs...")
for file in os.listdir(data_dir):
    if file.endswith('.csv'):
        base_name = file.replace('.csv', '')
        display_name = get_display_name(base_name)
        INDICATOR_MAPPING[display_name] = base_name
        print(f"Mapping créé : '{display_name}' -> '{base_name}'")
        
        datasets[base_name] = load_data(base_name)
        print(f"Données chargées pour {base_name}")

# Afficher le mapping pour débogage
print("\nMapping des indicateurs :")
for display_name, file_name in INDICATOR_MAPPING.items():
    print(f"- {display_name} -> {file_name}")

print("\nIndicateurs disponibles :")
for indicator in datasets.keys():
    print(f"- {indicator}")

# Définir l'indicateur par défaut
DEFAULT_INDICATOR = 'taux_de_fécondité'
DEFAULT_YEAR = 2020

# Initialiser l'application Dash avec le thème Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

# Créer la mise en page
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Tableau de bord des données démographiques mondiales",
                   className="text-center mb-4")
        ])
    ]),
    
    dbc.Row([
        dbc.Col([
            html.Label("Sélectionner un indicateur :"),
            dcc.Dropdown(
                id='indicator-selector',
                options=[{'label': get_display_name(k), 'value': k} 
                        for k in datasets.keys()],
                value=DEFAULT_INDICATOR
            ),
            html.Br(),
            html.Label("Sélectionner une année :"),
            dcc.Slider(
                id='year-slider',
                min=1960,  # Début à 1960 (données les plus anciennes disponibles)
                max=2025,  # Fin à 2025
                value=2020,  # Valeur par défaut
                marks={str(year): str(year) 
                       for year in range(1960, 2026, 5)},  # Marques tous les 5 ans
                step=1
            )
        ])
    ]),
    
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='world-map')
        ])
    ]),
    
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='time-series')
        ], width=8),
        dbc.Col([
            dcc.Graph(id='top-10-countries')
        ], width=4)
    ]),
    
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='population-evolution')
        ])
    ])
], fluid=True)

@app.callback(
    [Output('world-map', 'figure'),
     Output('time-series', 'figure'),
     Output('top-10-countries', 'figure'),
     Output('population-evolution', 'figure')],
    [Input('indicator-selector', 'value'),
     Input('year-slider', 'value')]
)
def update_figures(indicator, year):
    print(f"\nMise à jour des figures pour l'indicateur '{indicator}' et l'année {year}")
    
    if indicator not in datasets:
        print(f"Erreur : indicateur '{indicator}' non trouvé dans datasets")
        print("Indicateurs disponibles :", list(datasets.keys()))
        # Retourner des figures vides en cas d'erreur
        empty_fig = go.Figure()
        return empty_fig, empty_fig, empty_fig, empty_fig
    
    data = datasets[indicator]
    year_str = str(year)
    
    # Préparer les données pour la carte
    countries = []
    codes = []
    values = []
    
    if year in data['annee'].values:
        for index, row in data.iterrows():
            if row['annee'] == year:
                countries.append(row['pays'])
                codes.append(row['code_pays'])
                values.append(row['valeur'])
                
        print(f"Données pour la carte : {len(countries)} pays")
    else:
        print(f"Pas de données pour l'année {year}")
    
    if indicator == 'taux_de_mortalité':
        # Trier les pays par valeur décroissante et obtenir le top 10
        top_10 = data[data['annee'] == year].nlargest(10, 'valeur')
        # Créer une copie des données avec uniquement les valeurs pour le top 10
        df_colored = data[data['annee'] == year].copy()
        df_colored.loc[~df_colored['code_pays'].isin(top_10['code_pays']), 'valeur'] = None
        
        # Créer la carte avec les données filtrées
        fig_world_map = px.choropleth(df_colored,
                               locations='code_pays',
                               color='valeur',
                               hover_name='pays',
                               color_continuous_scale=COLOR_SCALES[indicator])
        
        # Ajouter les contours pour tous les pays
        fig_world_map.add_trace(
            go.Choropleth(
                locations=data[data['annee'] == year]['code_pays'],
                z=[1] * len(data[data['annee'] == year]),
                colorscale=[[0, 'rgba(0,0,0,0)'], [1, 'rgba(0,0,0,0)']],
                showscale=False,
                hoverinfo='skip',
                marker_line_color='gray',
                marker_line_width=0.5
            )
        )
    else:
        # Pour les autres indicateurs, afficher normalement
        fig_world_map = px.choropleth(data[data['annee'] == year],
                               locations='code_pays',
                               color='valeur',
                               hover_name='pays',
                               color_continuous_scale=COLOR_SCALES[indicator])
    
    fig_world_map.update_layout(
        title=f"{get_display_name(indicator)} par pays en {year}",
        coloraxis_colorbar_title=UNITS[indicator]
    )
    
    # Calculer les statistiques par année
    years = sorted(data['annee'].unique())
    avg_values = []
    min_values = []
    max_values = []
    min_countries = []
    max_countries = []
    
    for year in years:
        year_data = data[data['annee'] == year]
        if not year_data.empty:
            avg = year_data['valeur'].mean()
            min_val = year_data['valeur'].min()
            max_val = year_data['valeur'].max()
            
            # Trouver les pays avec les valeurs min et max
            min_country = year_data[year_data['valeur'] == min_val]['pays'].iloc[0]
            max_country = year_data[year_data['valeur'] == max_val]['pays'].iloc[0]
            
            avg_values.append(avg)
            min_values.append(min_val)
            max_values.append(max_val)
            min_countries.append(min_country)
            max_countries.append(max_country)
        else:
            avg_values.append(None)
            min_values.append(None)
            max_values.append(None)
            min_countries.append('')
            max_countries.append('')
    
    # Créer le graphique temporel avec les trois courbes
    fig_time_series = go.Figure()
    
    # Ajouter la courbe de la moyenne
    fig_time_series.add_trace(
        go.Scatter(
            x=years,
            y=avg_values,
            mode='lines',
            name='Moyenne mondiale',
            line=dict(color='blue', width=2),
            hovertemplate="Année: %{x}<br>" +
                         "Moyenne mondiale: %{y:.2f}<br>" +
                         "<extra></extra>"
        )
    )
    
    # Ajouter la courbe du minimum
    fig_time_series.add_trace(
        go.Scatter(
            x=years,
            y=min_values,
            mode='lines',
            name='Minimum',
            line=dict(color='red', width=2),
            hovertemplate="Année: %{x}<br>" +
                         "Minimum: %{y:.2f}<br>" +
                         "Pays: %{customdata}<br>" +
                         "<extra></extra>",
            customdata=min_countries
        )
    )
    
    # Ajouter la courbe du maximum
    fig_time_series.add_trace(
        go.Scatter(
            x=years,
            y=max_values,
            mode='lines',
            name='Maximum',
            line=dict(color='green', width=2),
            hovertemplate="Année: %{x}<br>" +
                         "Maximum: %{y:.2f}<br>" +
                         "Pays: %{customdata}<br>" +
                         "<extra></extra>",
            customdata=max_countries
        )
    )
    
    # Ajouter une zone ombrée entre min et max
    fig_time_series.add_trace(
        go.Scatter(
            x=years + years[::-1],
            y=max_values + min_values[::-1],
            fill='toself',
            fillcolor='rgba(0,100,80,0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            name='Plage de valeurs',
            showlegend=False,
            hoverinfo='skip'
        )
    )
    
    fig_time_series.update_layout(
        title=f"Évolution temporelle - {get_display_name(indicator)}",
        xaxis_title="Année",
        yaxis_title=UNITS[indicator],
        hovermode='x unified',
        showlegend=True
    )
    
    if year not in data['annee'].values:
        print(f"Pas de données pour l'année {year}")
        return fig_world_map, fig_time_series, go.Figure(), go.Figure()
    
    # Préparer les données pour le top 10
    countries = []
    values = []
    for index, row in data.iterrows():
        if row['annee'] == year:
            countries.append(row['pays'])
            values.append(row['valeur'])
    
    # Trier et prendre les 10 premiers
    sorted_data = sorted(zip(countries, values), key=lambda x: x[1], reverse=True)
    top_10 = sorted_data[:10]
    
    print(f"Top 10 calculé : {len(top_10)} pays")
    
    # Obtenir les couleurs de l'échelle définie pour cet indicateur
    if COLOR_SCALES[indicator] in px.colors.named_colorscales():
        colors = getattr(px.colors.sequential, COLOR_SCALES[indicator])  
    else:
        # Si l'échelle n'est pas dans les séquentielles, utiliser une échelle personnalisée
        if COLOR_SCALES[indicator] == 'RdYlBu':
            colors = px.colors.diverging.RdYlBu  
        elif COLOR_SCALES[indicator] == 'RdYlGn':
            colors = px.colors.diverging.RdYlGn  
        else:
            colors = px.colors.sequential.Viridis  
    
    # Calculer les couleurs pour chaque barre
    min_val = min(value for _, value in top_10)
    max_val = max(value for _, value in top_10)
    color_scale = []
    
    for _, value in top_10:
        # Normaliser la valeur entre 0 et 1
        if max_val != min_val:
            normalized = (value - min_val) / (max_val - min_val)
        else:
            normalized = 0.5
        # Sélectionner l'index de couleur correspondant
        color_idx = int(normalized * (len(colors) - 1))
        color_scale.append(colors[color_idx])
    
    fig_top_10 = go.Figure(data=[
        go.Bar(
            x=[country for country, _ in top_10],
            y=[value for _, value in top_10],
            marker_color=color_scale,
            hovertemplate="Pays: %{x}<br>" +
                         f"Valeur: %{{y:.2f}} {UNITS[indicator]}<br>" +
                         "<extra></extra>"
        )
    ])
    
    fig_top_10.update_layout(
        title=f"Top 10 pays - {get_display_name(indicator)} ({year})",
        xaxis_title="Pays",
        yaxis_title=UNITS[indicator],
        xaxis_tickangle=-45
    )
    
    if indicator == 'population_totale':
        evolution_fig = create_top10_evolution(data)
    else:
        evolution_fig = go.Figure()  # Figure vide pour les autres indicateurs
    
    return fig_world_map, fig_time_series, fig_top_10, evolution_fig

if __name__ == '__main__':
    print("Démarrage du tableau de bord...")
    print("Ouvrez votre navigateur à l'adresse : http://127.0.0.1:8050")
    app.run_server(debug=True)
