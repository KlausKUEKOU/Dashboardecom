# scraping.py
import requests
import time
import pandas as pd
from bs4 import BeautifulSoup

# --- Constantes communes ---
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}

# ---------------------------
# Scraping Amazon
# ---------------------------
def scrape_amazon():
    headers_amazon = {
        'User-Agent': HEADERS['User-Agent'],
        'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.amazon.fr/',
        'Connection': 'keep-alive'
    }
    urls = [
        'https://www.amazon.fr/s?k=ordinateur+portable',
        'https://www.amazon.fr/s?k=smartphone',
        'https://www.amazon.fr/s?k=smartwatch',
        'https://www.amazon.fr/s?k=airpods'
    ]
    all_data = []
    for url in urls:
        try:
            response = requests.get(url, headers=headers_amazon, timeout=100)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            if "amazon.fr" in url:
                site = "Amazon"
                items = soup.select('.s-result-item')
                for item in items:
                    title = item.select_one('div.a-section.a-spacing-none.a-spacing-top-small.s-title-instructions-style > a > h2 > span')
                    price = item.select_one('span.a-offscreen')
                    rating = item.select_one('span.a-icon-alt')
                    reviews = item.select_one('span.a-size-base.s-underline-text')
                    stock = item.select_one('span.a-size-base.a-color-price')
                    promo = item.select_one('span.a-price.a-text-price > span:nth-child(2)')
                    title_text = title.text.strip() if title else None
                    price_text = price.text.strip().replace('€', '').replace(',', '.') if price else "0"
                    rating_text = rating.text.split()[0].replace(',', '.') if rating else "0"
                    reviews_text = reviews.text.replace('(', '').replace(')', '').replace(',', '') if reviews else "0"
                    promo_text = promo.text.replace('€', '').replace(',', '.') if promo else "0"
                    stock_text = stock.text.strip() if stock else 'Disponible'
                    if title_text:
                        all_data.append({
                            'Site': site,
                            'Titre': title_text,
                            'Prix_euro': price_text,
                            'Note': rating_text,
                            'Avis': reviews_text,
                            'Promo': promo_text,
                            'Stock': stock_text
                        })
        except Exception as e:
            print(f"❌ Erreur lors du scraping d'Amazon ({url}): {e}")
        time.sleep(2)
    return pd.DataFrame(all_data)

# ---------------------------
# Scraping Boulanger
# ---------------------------
def scrape_boulanger(url, produit):
    headers_boulanger = HEADERS
    all_data = []
    try:
        response = requests.get(url, headers=headers_boulanger, timeout=900)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        items = soup.select('#product-list > ul > li > article')
        for item in items:
            title = item.select_one('#productLabel')
            price = item.select_one('.product-list__product-area-3.g-col-5.g-col-sm-7.g-col-md-4.g-start-md-9.g-col-lg-3.g-start-lg-7.g-col-xl-3.g-start-xl-7 > div > p')
            rating = item.select_one('.product-list__product-area-2.g-col-5.g-col-sm-7.g-col-md-4.g-col-lg-3.g-col-xl-3 > div.product-list__product-rating > a > div > bl-rating')
            reviews = item.select_one('.product-list__product-area-2.g-col-5.g-col-sm-7.g-col-md-4.g-col-lg-3.g-col-xl-3 > div.product-list__product-rating > a > span')
            promo = item.select_one('.product-list__product-area-3.g-col-5.g-col-sm-7.g-col-md-4.g-start-md-9.g-col-lg-3.g-start-lg-7.g-col-xl-3.g-start-xl-7 > div > div > span.price__crossed')
            stock = item.select_one('.product-list__product-area-3.g-col-5.g-col-sm-7.g-col-md-4.g-start-md-9.g-col-lg-3.g-start-lg-7.g-col-xl-3.g-start-xl-7 > button > span')
            if title and price:
                all_data.append({
                    'Titre': title.text.strip(),
                    'Prix_euro': price.text.replace(',', '.').strip(),
                    'Note': rating.get('rating') if rating else "0",
                    'Avis': reviews.text.strip() if reviews else "0",
                    'Promo': promo.text.strip() if promo else "0",
                    'Stock': 'Disponible' if stock else 'Indisponible',
                    'Produit': produit,
                    'Site': 'Boulanger'
                })
        print(f"✅ Boulanger ({produit}): {len(items)} produits trouvés")
    except Exception as e:
        print(f"❌ Erreur lors du scraping de Boulanger ({produit}): {e}")
    time.sleep(2)
    return pd.DataFrame(all_data)

def scrape_boulanger_all():
    df_smartphone = scrape_boulanger("https://www.boulanger.com/c/smartphone-telephone-portable", "Smartphone")
    df_laptop = scrape_boulanger("https://www.boulanger.com/c/tous-les-ordinateurs-portables", "Laptop")
    df_airpods = scrape_boulanger("https://www.boulanger.com/c/airpods", "Airpods")
    df_smartwatch = scrape_boulanger("https://www.boulanger.com/c/montre-connectee", "Smartwatch")
    return pd.concat([df_smartphone, df_laptop, df_airpods, df_smartwatch], ignore_index=True)

# ---------------------------
# Scraping Jumia
# ---------------------------
def scrape_jumia():
    headers_jumia = {
        'User-Agent': HEADERS['User-Agent'],
        'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.jumia.com.ng/',
        'Connection': 'keep-alive'
    }
    urls = [
        'https://www.jumia.com.ng/catalog/?q=smartwatch',
        'https://www.jumia.com.ng/catalog/?q=smartphone',
        'https://www.jumia.com.ng/catalog/?q=airpods',
        'https://www.jumia.com.ng/catalog/?q=laptops'
    ]
    all_data = []
    for url in urls:
        try:
            response = requests.get(url, headers=headers_jumia, timeout=1000)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            if "jumia.com.ng" in url:
                site = "Jumia"
                items = soup.select('#jm > main > div.aim.row.-pbm > div.-pvs.col12 > section > div > article')
                for item in items:
                    title = item.select_one('h3')
                    price = item.select_one('div.prc')
                    rating = item.select_one('div.rev > div')
                    reviews = item.select_one('div.rev')
                    discount = item.select_one('div.bdg._dsct._sm')
                    title_text = title.text.strip() if title else "N/A"
                    price_text = price.text.strip() if price else "N/A"
                    rating_text = rating.text.strip() if rating else "N/A"
                    reviews_text = reviews.text.strip() if reviews else "0"
                    stock_text = "Non renseigné"
                    discount_text = discount.text.strip() if discount else "Aucun rabais"
                    if title_text and price_text:
                        all_data.append({
                            'Site': site,
                            'Titre': title_text,
                            'Prix_euro': price_text,
                            'Note': rating_text.replace('out of 5', ''),
                            'Avis': reviews_text,
                            'Stock': stock_text,
                            'Promo': discount_text
                        })
        except Exception as e:
            print(f"❌ Erreur lors du scraping de Jumia ({url}): {e}")
        time.sleep(2)
    return pd.DataFrame(all_data)

# ---------------------------
# Scraping Materiel.net
# ---------------------------
def scrape_materiel():
    all_data = []
    urls = [
        'https://www.materiel.net/recherche/smartphone/',
        'https://www.materiel.net/recherche/ordinateur%20portable/',
        'https://www.materiel.net/recherche/smartwatch/',
        'https://www.materiel.net/recherche/airpods/'
    ]
    for url in urls:
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            items = soup.select('.c-products-list__item')
            for item in items:
                title = item.select_one('.c-product__title')
                price = item.select_one('.o-product__price')
                description = item.select_one('.c-product__description')
                dispo = item.select_one('.o-availability__value')
                title_text = title.text.strip() if title else None
                price_text = price.text.strip().replace('€', '.').replace(' ', '') if price else None
                description_text = description.text.strip() if description else None
                dispo_text = dispo.text.strip() if dispo else "0"
                if title_text and price_text:
                    # Déduire le type de produit selon l'URL
                    produit = "Autre"
                    if "smartphone" in url:
                        produit = "Smartphone"
                    elif "ordinateur" in url:
                        produit = "Laptop"
                    elif "smartwatch" in url:
                        produit = "Smartwatch"
                    elif "airpods" in url:
                        produit = "AirPods"
                    all_data.append({
                        'Site': 'Materiel.net',
                        'Titre': title_text,
                        'Prix_euro': price_text,
                        'Note': 0,
                        'Avis': 0,
                        'Promo': 0,
                        'Stock': dispo_text,
                        'Produit': produit,
                        'Description': description_text
                    })
        except Exception as e:
            print(f"❌ Erreur lors du scraping de Materiel.net ({url}): {e}")
        time.sleep(2)
    return pd.DataFrame(all_data)

# ---------------------------
# Scraping LDLC
# ---------------------------
def scrape_ldlc():
    all_data = []
    urls = [
        'https://www.ldlc.com/recherche/smartphone/',
        'https://www.ldlc.com/recherche/ordinateur/',
        'https://www.ldlc.com/recherche/smartwatch/',
        'https://www.ldlc.com/recherche/airpods/'
    ]
    for url in urls:
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            items = soup.select('.pdt-item')
            for item in items:
                title = item.select_one('.title-3')
                price = item.select_one('.new-price')
                if not price:
                    price = item.select_one('.price')
                description = item.select_one('.desc')
                dispo = item.select_one('.stock')
                title_text = title.text.strip() if title else None
                price_text = price.text.strip().replace('€', '.').replace(' ', '') if price else None
                description_text = description.text.strip() if description else None
                dispo_text = dispo.text.strip() if dispo else "0"
                if title_text and price_text:
                    produit = "Autre"
                    if "smartphone" in url:
                        produit = "Smartphone"
                    elif "ordinateur" in url:
                        produit = "Laptop"
                    elif "smartwatch" in url:
                        produit = "Smartwatch"
                    elif "airpods" in url:
                        produit = "AirPods"
                    all_data.append({
                        'Site': 'LDLC',
                        'Titre': title_text,
                        'Prix_euro': price_text,
                        'Note': 0,
                        'Avis': 0,
                        'Promo': 0,
                        'Stock': dispo_text,
                        'Produit': produit,
                        'Description': description_text
                    })
        except Exception as e:
            print(f"❌ Erreur lors du scraping de LDLC ({url}): {e}")
        time.sleep(2)
    return pd.DataFrame(all_data)

# ---------------------------
# Fonctions de Nettoyage
# ---------------------------
def nettoyer_base_de_donnees1(df):
    # Pour Amazon
    df.columns = ['Site', 'Titre', 'Prix_euro', 'Note', 'Avis', 'Promo', 'Stock']
    df['Prix_euro'] = df['Prix_euro'].astype(str).str.replace('\u202f', '').str.replace('\xa0', '').astype(float)
    df['Note'] = df['Note'].astype(float)
    df['Avis'] = df['Avis'].astype(str).str.replace('\xa0', '').astype(int)
    df['Promo'] = ((df['Promo'].astype(str).str.replace('\u202f', '').str.replace('\xa0', '').astype(float)) - df['Prix_euro']) / (
                    df['Promo'].astype(str).str.replace('\u202f', '').str.replace('\xa0', '').astype(float))
    return df[['Site', 'Titre', 'Prix_euro', 'Note', 'Avis', 'Promo', 'Stock']]

 
def nettoyer_base_de_donnees(df):
    # Si le DataFrame contient une colonne indésirable (par exemple 'Prix (€)' au lieu de 'Prix_euro'),
    # on la renomme. On adapte aussi la structure en conservant éventuellement la colonne 'Produit'.
    mapping = {
        "Prix (€)": "Prix_euro"
    }
    df = df.rename(columns=mapping)

    # Définir l'ordre souhaité des colonnes.
    # Si 'Produit' existe, on l'inclut dans l'ordre ; sinon, on la laisse de côté.
    colonnes_souhaitees = ['Titre', 'Prix_euro', 'Note', 'Avis', 'Promo', 'Stock']
    if 'Produit' in df.columns:
        colonnes_souhaitees.insert(1, 'Produit')  # Par exemple, ordre: Titre, Produit, Prix_euro, ...
    
    # Extraire uniquement les colonnes attendues (si le DataFrame contient d'autres colonnes, on les ignore)
    df = df[colonnes_souhaitees].copy()

    # Conversion et nettoyage des colonnes numériques
    df['Prix_euro'] = df['Prix_euro'].astype(str).str.replace('€', '').str.replace(',', '.').astype(float)
    df['Note'] = df['Note'].astype(float)
    df['Avis'] = df['Avis'].astype(str).str.extract(r'\((\d+)\)').fillna(0).astype(int)
    df['Promo'] = ((df['Promo'].astype(str)
                     .str.replace('€', '')
                     .str.replace(',', '.')
                     .astype(float)) - df['Prix_euro']) / (df['Promo'].astype(str)
                                                            .str.replace('€', '')
                                                            .str.replace(',', '.')
                                                            .astype(float))
    # Assigner la valeur du site
    df['Site'] = 'Boulanger'
    
    # Réordonner les colonnes pour le rendu final
    colonnes_finales = ['Site'] + colonnes_souhaitees
    return df[colonnes_finales]


def nettoyer_jumia(df):
    df.columns = ['Site', 'Titre', 'Prix_euro', 'Note', 'Avis', 'Stock', 'Promo']
    df['Prix_euro'] = (df['Prix_euro'].astype(str)
                        .str.replace('₦', '')
                        .str.replace('e', '')
                        .str.replace(',', '')
                        .str.strip())
    def convert_price(price):
        if '-' in price:
            prices = price.split('-')
            prices = [float(p.strip()) for p in prices]
            return sum(prices) / 2
        else:
            return price
    df['Prix_euro'] = df['Prix_euro'].apply(convert_price).astype(float) * 0.00063
    df['Note'] = df['Note'].replace('N/A', 0).fillna(0).astype(float)
    df['Avis'] = df['Avis'].str.extract(r'\((\d+)\)').fillna(0).astype(int)
    df['Promo'] = (df['Promo'].str.replace('%', '').str.replace('Aucun rabais', '0').str.strip().astype(float)) * 0.01
    return df[['Site', 'Titre', 'Prix_euro', 'Note', 'Avis', 'Promo', 'Stock']]

# Fonction pour classifier les produits
def classify_product(title):
    title_lower = str(title).lower()  # Convertir en minuscules pour uniformiser la recherche
    if 'smart watch' in title_lower or 'smartwatch' in title_lower:
        return 'Smartwatch'
    elif 'smartphone' in title_lower or 'android' in title_lower or 'redmi' in title_lower or 'sim' in title_lower or 'itel' in title_lower or 'zte' in title_lower:
        return 'Smartphone'
    elif 'airpods' in title_lower or 'pods' in title_lower or 'earphone' in title_lower or 'ear' in title_lower:
        return 'AirPods'
    elif 'laptop' in title_lower or 'book' in title_lower or 'pc' in title_lower or 'intel' in title_lower or 'dell' in title_lower or 'hp' in title_lower:
        return 'Laptop'
    else:
        return 'Autre'

def classify_product1(title):
    title_lower = str(title).lower()  # Convertir en minuscules pour uniformiser la recherche
    if 'smart watch' in title_lower or 'smartwatch' in title_lower or 'montre' in title_lower or 'connectée' in title_lower:
        return 'Smartwatch'
    elif 'smartphone' in title_lower or 'telephone' in title_lower or 'redmi' in title_lower or 'sim' in title_lower or 'itel' in title_lower or 'zte' in title_lower:
        return 'Smartphone'
    elif 'airpods' in title_lower or 'écouteur' in title_lower or 'earphone' in title_lower or 'casque' in title_lower:
        return 'AirPods'
    elif 'laptop' in title_lower or 'book' in title_lower or 'pc' in title_lower or 'intel' in title_lower or 'ordinateur' in title_lower  or 'portable' in title_lower:
        return 'Laptop'
    else:
        return 'Autre'

# ---------------------------
# Fonction Globale de Chargement
# ---------------------------
def charger_donnees():
    print("🔎 Scraping Amazon...")
    ama = scrape_amazon()
    
    print("🔎 Scraping Boulanger...")
    boulanger_df = scrape_boulanger_all()
    
    print("🔎 Scraping Jumia...")
    jumia_df = scrape_jumia()
    
    print("🔎 Scraping Materiel.net...")
    materiel_df = scrape_materiel()
    
    print("🔎 Scraping LDLC...")
    ldlc_df = scrape_ldlc()
    
    # Nettoyage spécifique à chaque source
    ama_clean = nettoyer_base_de_donnees1(ama) if not ama.empty else ama
    boulanger_clean = nettoyer_base_de_donnees(boulanger_df) if not boulanger_df.empty else boulanger_df
    jumia_clean = nettoyer_jumia(jumia_df) if not jumia_df.empty else jumia_df
    jumia_clean['Produit'] = jumia_clean['Titre'].apply(classify_product)
    ama_clean['Produit'] = ama_clean['Titre'].apply(classify_product1)
    # Pour Materiel.net et LDLC, vous pouvez ajouter des étapes de nettoyage selon vos besoins.
    
    # Concaténation finale
    df_final = pd.concat([ama_clean, boulanger_clean, jumia_clean, materiel_df, ldlc_df], ignore_index=True)
    df_final['Produit'] = df_final['Produit'].replace('Airpods', 'AirPods')
    return df_final
