# Web Scraping et Dashboard d'Analyse E-commerce

## Introduction

### Objectif du Projet
Ce projet a pour objectif de collecter des données provenant de plusieurs plateformes e-commerce (Amazon, Boulanger, Jumia, LDLC, Materiel.net) afin d'analyser :
- La concurrence entre les plateformes,
- Les promotions en cours,
- Les stocks disponibles,
- L'évolution des prix,
- Les produits les mieux notés,
- Les produits ayant le plus grand nombre d'avis.

Ces analyses sont regroupées dans un **dashboard interactif** construit avec **Streamlit**, offrant une visualisation claire et intuitive des tendances du marché.

### Contexte
Dans un marché e-commerce en constante évolution, il est essentiel de comprendre les dynamiques concurrentielles, les stratégies de prix et les préférences des consommateurs. Ce projet permet de répondre à ces enjeux en fournissant des insights basés sur des données actualisées et analysées.

---

## Fonctionnalités du Projet
1. **Web Scraping** :
   - Collecte de données sur les produits (prix, promotions, stocks, avis, etc.) à partir des plateformes suivantes :
     - Amazon
     - Boulanger
     - Jumia
     - LDLC
     - Materiel.net
   - Utilisation de bibliothèques Python telles que `BeautifulSoup`.

2. **Analyse des Données** :
   - Nettoyage et traitement des données collectées.
   - Calcul des indicateurs clés (évolution des prix, produits populaires, etc.).

3. **Dashboard Interactif** :
   - Construction d'un dashboard avec **Streamlit**.
   - Visualisations interactives (graphiques, tableaux, filtres, etc.).
   - Options pour explorer les données par plateforme, catégorie de produit, ou période.

---

## Difficultés Rencontrées et Mesures Palliatives

### 1. **Problèmes de Web Scraping**
#### Difficultés :
- **Données incomplètes** : Certaines informations (comme les stocks ou les promotions) ne sont pas toujours disponibles ou sont difficiles à extraire.

#### Mesures Palliatives :
- Implémentation de **valeurs par défaut** pour les données manquantes et utilisation de techniques de nettoyage pour garantir la cohérence des données.

---

### 2. **Traitement des Données**
#### Difficultés :
- **Hétérogénéité des données** : Les données collectées proviennent de sources différentes avec des formats variés (prix en différentes devises, promotions formulées différemment, etc.).
- **Données bruyantes** : Présence de caractères spéciaux, d'espaces insécables, ou de formats incorrects (par exemple, `1\xa0829.95` pour un prix).

#### Mesures Palliatives :
- Normalisation des données (par exemple, conversion des prix en une seule devise, standardisation des formats de date).
- Utilisation de **expressions régulières (regex)** pour nettoyer les données bruyantes.
- Implémentation de scripts de **validation des données** pour détecter et corriger les incohérences.

---

### 3. **Performance du Dashboard**
#### Difficultés :
- **Latence lors de la visualisation** : Le chargement des données volumineuses dans le dashboard Streamlit peut ralentir l'interface.
- **Limites de Streamlit** : Streamlit recharge l'ensemble de l'application à chaque interaction, ce qui peut être inefficace pour des datasets importants.

#### Mesures Palliatives :
- Utilisation de **mémoization** avec `@st.cache_data` pour éviter de recalculer les données à chaque interaction.
- Limitation du nombre de données affichées en temps réel et ajout de filtres pour réduire la charge.

---

### 4. **Visualisation des Données**
#### Difficultés :
- **Choix des graphiques** : Trouver les visualisations les plus adaptées pour représenter des données complexes (par exemple, l'évolution des prix sur plusieurs plateformes).
- **Interactivité** : Rendre les graphiques interactifs tout en gardant une interface simple et intuitive.

#### Mesures Palliatives :
- Utilisation de bibliothèques de visualisation comme **Plotly** pour des graphiques interactifs et personnalisables.
- Conception d'une interface utilisateur intuitive avec des filtres et des options de personnalisation pour permettre aux utilisateurs d'explorer les données facilement.

## Installation et Utilisation

### Prérequis
- Python 3.8 ou supérieur
- Bibliothèques Python : voir `requirements.txt`
     - **`requests`** : Pour effectuer des requêtes HTTP et récupérer le contenu des pages web.
     - **`BeautifulSoup`** : Pour analyser et parser le contenu HTML des pages.
     - **`pandas`** : Pour organiser les données collectées dans un DataFrame.
  
### Étapes d'Installation
- cd chemin/vers/projet-ecommerce
- pip install -r requirements.txt
- streamlit run app.py
- http://localhost:8501












