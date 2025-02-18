import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Choisir une page", [
    "Accueil",
    "Analyse de la Concurrence",
    "Analyse des Promotions",
    "Analyse des Stocks",
    "Évolution des Prix",
    "Produits les Mieux Notés",
    "Produits avec le Plus d'Avis",
    "Comparaison des Prix"
])

# Valeurs par défaut pour Top/Bottom N
top_n = st.sidebar.slider("Sélectionner le nombre de produits pour Top/Bottom N", min_value=1, max_value=10, value=5)
# Page d'accueil
if selected_page == "Accueil":
    st.title("Dashboard des Sites E-commerce")
    st.write("Bienvenue sur le tableau de bord interactif !")
    st.dataframe(df)

# Page 1: Analyse de la Concurrence
if page == "Analyse de la Concurrence":
    st.title("📊 Analyse de la Concurrence entre Sites")

    # Value Box : Nombre total de produits
    st.metric(label="Nombre Total de Produits", value=len(df))

        # Tableau Récapitulatif : Prix moyen par site
    avg_prices = df.groupby('Site').agg({
        'Titre' : 'count',
        'Prix_euro': 'mean',  
        'Avis': 'mean',       
        'Note': 'mean'       
    }).reset_index()

    # Renommer les colonnes pour une meilleure lisibilité
    avg_prices.columns = ['Site', 'Total produit', 'Prix Moyen euro', 'Nombre Moyen d\'Avis', 'Note Moyenne']

    # Afficher le tableau récapitulatif
    st.write("### Tableau Récapitulatif : Prix Moyen, Nombre Moyen d'Avis et Note Moyenne par Site")
    st.table(avg_prices.style.format({
        'Total produit': '{:.2f}',
        'Prix Moyen euro': '{:.2f}',  
        'Nombre Moyen d\'Avis': '{:.0f}',  
        'Note Moyenne': '{:.2f}'     
    }))

    # Ajouter des graphiques sur la même ligne
    st.write("### Comparaison Graphique entre les Sites")

    # Créer 4 colonnes pour afficher les graphiques côte à côte
    col1, col2, col3, col4 = st.columns(4)

    # Nuage de points 1 : Prix Moyen vs Total Produits
    with col1:
        fig1 = px.scatter(
            avg_prices,
            x='Total Produits',
            y='Prix Moyen euro',
            color='Site',
            title="Prix Moyen vs Total Produits",
            labels={'Prix Moyen euro': 'Prix Moyen (€)', 'Total Produits': 'Nombre de Produits'},
            hover_name='Site'
        )
        fig1.update_layout(width=350, height=350)
        st.plotly_chart(fig1)

    # Nuage de points 2 : Nombre Moyen d'Avis vs Prix Moyen
    with col2:
        fig2 = px.scatter(
            avg_prices,
            x='Prix Moyen euro',
            y='Nombre Moyen d\'Avis',
            color='Site',
            title="Nombre Moyen d'Avis vs Prix Moyen",
            labels={'Nombre Moyen d\'Avis': 'Nombre Moyen d\'Avis', 'Prix Moyen euro': 'Prix Moyen (€)'},
            hover_name='Site'
        )
        fig2.update_layout(width=350, height=350)
        st.plotly_chart(fig2)

    # Nuage de points 3 : Note Moyenne vs Nombre Moyen d'Avis
    with col3:
        fig3 = px.scatter(
            avg_prices,
            x='Nombre Moyen d\'Avis',
            y='Note Moyenne',
            color='Site',
            title="Note Moyenne vs Nombre Moyen d'Avis",
            labels={'Nombre Moyen d\'Avis': 'Nombre Moyen d\'Avis', 'Note Moyenne': 'Note Moyenne'},
            hover_name='Site'
        )
        fig3.update_layout(width=350, height=350)
        st.plotly_chart(fig3)

    # Nuage de points 4 : Total Produits vs Note Moyenne
    with col4:
        fig4 = px.scatter(
            avg_prices,
            x='Total Produits',
            y='Note Moyenne',
            color='Site',
            title="Note Moyenne vs Total Produits",
            labels={'Total Produits': 'Nombre de Produits', 'Note Moyenne': 'Note Moyenne'},
            hover_name='Site'
        )
        fig4.update_layout(width=350, height=350)
        st.plotly_chart(fig4)

    col1, col2 = st.columns(2)

    with col1 :
        # Top N et Bottom N produits par site
        st.write(f"### Top {top_n} Produits par Site")
        top_products = df.sort_values(by='Prix_euro', ascending=False).groupby('Site').head(top_n)
        st.table(top_products[['Site', 'Titre', 'Prix_euro', 'Produit']])
    with col2 :
        st.write(f"### Bottom {top_n} Produits par Site")
        bottom_products = df.sort_values(by='Prix_euro').groupby('Site').head(top_n)
        st.table(bottom_products[['Site', 'Titre', 'Prix_euro', 'Produit']])

# Page 2: Analyse des Promotions
elif page == "Analyse des Promotions":
    st.title("🎉 Analyse des Promotions")

    # Filtrer les produits en promotion
    promo_df = df[df['Promo'] > 0]

    # Value Box : Nombre total de produits en promotion
    st.metric(label="Nombre de Produits en Promotion", value=len(promo_df))

    # Tableau Récapitulatif : Taux de rabais moyen par site
    avg_promo = promo_df.groupby('Site')['Promo'].mean().reset_index()
    avg_promo.columns = ['Site', 'Taux de Rabais Moyen (%)']
    st.write("### Tableau Récapitulatif : Taux de Rabais Moyen par Site")
    st.table(avg_promo)

    # Graphique : Taux de rabais par produit
    fig_promo = px.bar(
        promo_df,
        x='Titre',
        y='Promo',
        color='Site',
        title=f"Taux de Rabais pour les Produits en Promotion (Top {top_n})",
        labels={'Promo': 'Taux de Rabais (%)', 'Titre': 'Produit'}
    )
    st.plotly_chart(fig_promo)
    col1, col2 = st.columns(2)
        # Top N et Bottom N produits en promotion
    with col1 :
        st.write(f"### Top {top_n} Produits en Promotion (Plus Grand Rabais)")
        top_promo = promo_df.sort_values(by='Promo', ascending=False).head(top_n)
        st.table(top_promo[['Site', 'Titre', 'Prix_euro', 'Promo']])
    with col2 : 
        st.write(f"### Bottom {top_n} Produits en Promotion (Plus Petit Rabais)")
        bottom_promo = promo_df.sort_values(by='Promo').head(top_n)
        st.table(bottom_promo[['Site', 'Titre', 'Prix_euro', 'Promo']])

# Page 3: Analyse des Stocks
elif page == "Analyse des Stocks":
    st.title("📦 Analyse des Stocks")

    # Value Box : Pourcentage de produits disponibles
    total_products = len(df)
    available_products = len(df[df['Stock'] == 'disponible'])
    unavailable_products = len(df[df['Stock'] == 'non disponible'])
    st.metric(label="Pourcentage de Produits Disponibles", value=f"{(available_products / total_products * 100):.2f}%")
    st.metric(label="Pourcentage de Produits Indisponibles", value=f"{(unavailable_products / total_products * 100):.2f}%")

    # Tableau Récapitulatif : Répartition des stocks par site
    stock_summary = df.groupby(['Site', 'Stock']).size().unstack(fill_value=0).reset_index()
    stock_summary.columns = ['Site', 'Disponible', 'Indisponible']
    st.write("### Tableau Récapitulatif : Répartition des Stocks par Site")
    st.table(stock_summary)

    # Graphique : Répartition des stocks par site
    fig_stock = px.bar(
        stock_summary.melt(id_vars=['Site'], value_vars=['Disponible', 'Indisponible']),
        x='Site',
        y='value',
        color='variable',
        title="Répartition des Stocks par Site",
        labels={'value': 'Nombre de Produits', 'variable': 'Statut du Stock'},
        barmode='group'
    )
    st.plotly_chart(fig_stock)

    col1, col2 = st.columns(2)
        # Top N et Bottom N produits selon leur disponibilité
    with col1 : 
        st.write(f"### Top {top_n} Produits Disponibles")
        top_available = df[df['Stock'] == 'disponible'].sort_values(by='Avis', ascending=False).head(top_n)
        st.table(top_available[['Site', 'Titre', 'Prix_euro', 'Stock', 'Avis']])
    with col2 :
        st.write(f"### Bottom {top_n} Produits Indisponibles")
        bottom_unavailable = df[df['Stock'] == 'non disponible'].sort_values(by='Avis').head(top_n)
        st.table(bottom_unavailable[['Site', 'Titre', 'Prix_euro', 'Stock', 'Avis']])

# Page 4: Évolution des Prix
elif page == "Évolution des Prix":
    st.title("📈 Évolution des Prix par Produit")

    # Sélectionner un produit spécifique
    selected_product = st.selectbox("Sélectionnez un produit :", df['Produit'].unique())
    product_data = df[df['Produit'] == selected_product]

    if not product_data.empty:
        # Value Box : Prix avant 
        mean_price = product_data['Prix_euro'].iloc[0]
        st.metric(label="Prix", value=f"€{mean_price:.2f}")

        metrics_by_site = product_data.groupby('Site')['Prix_euro'].agg(['mean', 'median', 'min', 'max']).reset_index()
        metrics_by_site.columns = ['Site', 'Prix Moyen', 'Prix Médian', 'Prix Min', 'Prix Max']

        # Créer une ligne avec 4 colonnes pour les graphiques
        col1, col2, col3, col4 = st.columns(4)

        # Camembert 1 : Prix Moyen par Site
        with col1:
            fig_prix_moyen = go.Figure(
                go.Pie(
                    labels=metrics_by_site['Site'],
                    values=metrics_by_site['Prix Moyen'],
                    title="Prix Moyen"
                )
            )
            fig_prix_moyen.update_layout(width=350, height=350, margin=dict(t=50, b=10, l=10, r=10))
            st.plotly_chart(fig_prix_moyen)

        # Camembert 2 : Prix Médian par Site
        with col2:
            fig_prix_median = go.Figure(
                go.Pie(
                    labels=metrics_by_site['Site'],
                    values=metrics_by_site['Prix Médian'],
                    title="Prix Médian"
                )
            )
            fig_prix_median.update_layout(width=350, height=350, margin=dict(t=50, b=10, l=10, r=10))
            st.plotly_chart(fig_prix_median)

        # Nuage de Points 1 : Prix Min par Site
        with col3:
            fig_prix_min = px.scatter(
                metrics_by_site,
                x='Site',
                y='Prix Min',
                color='Site',
                title="Prix Minimum",
                labels={'Prix Min': 'Prix Min (€)', 'Site': 'Site'}
            )
            fig_prix_min.update_layout(width=350, height=350, margin=dict(t=50, b=10, l=10, r=10))
            st.plotly_chart(fig_prix_min)

        # Nuage de Points 2 : Prix Max par Site
        with col4:
            fig_prix_max = px.scatter(
                metrics_by_site,
                x='Site',
                y='Prix Max',
                color='Site',
                title="Prix Maximum",
                labels={'Prix Max': 'Prix Max (€)', 'Site': 'Site'}
            )
            fig_prix_max.update_layout(width=350, height=350, margin=dict(t=50, b=10, l=10, r=10))
            st.plotly_chart(fig_prix_max)

        # Afficher un tableau récapitulatif des métriques
        st.subheader(f"Tableau Récapitulatif des Prix pour '{selected_product}'")
        st.table(metrics_by_site.style.format({
            'Prix Moyen': '{:.2f}',
            'Prix Médian': '{:.2f}',
            'Prix Min': '{:.2f}',
            'Prix Max': '{:.2f}'
        }))
    else:
        st.warning("Aucune donnée disponible pour ce produit.")

# Page 5: Produits les Mieux Notés
elif page == "Produits les Mieux Notés":
    st.title("🌟 Produits les Mieux Notés")

    # Value Box : Note moyenne globale
    avg_rating = df['Note'].mean()
    st.metric(label="Note Moyenne Globale", value=f"{avg_rating:.2f}")

    # Top N produits mieux notés
    st.write(f"### Top {top_n} Produits Mieux Notés")
    top_rated = df.sort_values(by='Note', ascending=False).head(top_n)
    st.table(top_rated[['Site', 'Titre', 'Prix_euro', 'Note', 'Avis']])

    # Bottom N produits moins bien notés
    st.write(f"### Bottom {top_n} Produits Moins Bien Notés")
    bottom_rated = df.sort_values(by='Note').head(top_n)
    st.table(bottom_rated[['Site', 'Titre', 'Prix_euro', 'Note', 'Avis']])

# Page 6: Produits avec le Plus d'Avis
elif page == "Produits avec le Plus d'Avis":
    st.title("💬 Produits avec le Plus d'Avis")

    # Value Box : Nombre total d'avis
    total_reviews = df['Avis'].sum()
    st.metric(label="Nombre Total d'Avis", value=total_reviews)

    # Top N produits avec le plus d'avis
    st.write(f"### Top {top_n} Produits avec le Plus d'Avis")
    top_reviews = df.sort_values(by='Avis', ascending=False).head(top_n)
    st.table(top_reviews[['Site', 'Titre', 'Prix_euro', 'Note', 'Avis']])

    # Bottom N produits avec le moins d'avis
    st.write(f"### Bottom {top_n} Produits avec le Moins d'Avis")
    bottom_reviews = df.sort_values(by='Avis').head(top_n)
    st.table(bottom_reviews[['Site', 'Titre', 'Prix_euro', 'Note', 'Avis']])

# Page 7: Comparaison des Prix
elif page == "Comparaison des Prix":
    st.title("💰 Comparaison des Prix entre Sites")

    # Value Box : Prix minimum et maximum
    min_price = df['Prix_euro'].min()
    max_price = df['Prix_euro'].max()
    st.metric(label="Prix Minimum", value=f"€{min_price:.2f}")
    st.metric(label="Prix Maximum", value=f"€{max_price:.2f}")

    # Tableau Récapitulatif : Prix par site
    price_summary = df.groupby('Site')['Prix_euro'].agg(['min', 'max', 'mean']).reset_index()
    price_summary.columns = ['Site', 'Prix Minimum (€)', 'Prix Maximum (€)', 'Prix Moyen (€)']
    st.write("### Tableau Récapitulatif : Prix par Site")
    st.table(price_summary)

    # Graphique : Boîtes à moustaches pour comparer les prix
    fig_box = px.box(
        df,
        x='Site',
        y='Prix_euro',
        title="Comparaison des Prix entre Sites",
        labels={'Prix_euro': 'Prix (€)', 'Site': 'Site'}
    )
    st.plotly_chart(fig_box)

    # Top N et Bottom N produits selon le prix
    st.write(f"### Top {top_n} Produits les Plus Chers")
    top_expensive = df.sort_values(by='Prix_euro', ascending=False).head(top_n)
    st.table(top_expensive[['Site', 'Titre', 'Prix_euro', 'Note', 'Avis']])

    st.write(f"### Bottom {top_n} Produits les Moins Chers")
    bottom_cheapest = df.sort_values(by='Prix_euro').head(top_n)
    st.table(bottom_cheapest[['Site', 'Titre', 'Prix_euro', 'Note', 'Avis']])
