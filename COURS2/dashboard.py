from flask import Flask, render_template
import sqlite3
import os
from datetime import datetime, date

app = Flask(__name__)

# Chemin où sont stockés les QR codes
QR_FOLDER = "static/qr_codes"

@app.route("/")
def index():
    # Connexion à la base SQLite
    conn = sqlite3.connect("poids.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, poids, date, rayon FROM mesures")
    produits = cursor.fetchall()
    
    # Calculer les statistiques
    nb_produits = len(produits)
    
    # Entrées d'aujourd'hui
    today = date.today().strftime('%Y-%m-%d')
    cursor.execute("SELECT COUNT(*) FROM mesures WHERE date LIKE ?", (f"{today}%",))
    entrees_aujourdhui = cursor.fetchone()[0]
    
    # Statistiques de poids
    cursor.execute("SELECT AVG(poids), MIN(poids), MAX(poids) FROM mesures")
    stats = cursor.fetchone()
    poids_moyen = round(stats[0], 2) if stats[0] else 0
    poids_min = round(stats[1], 2) if stats[1] else 0
    poids_max = round(stats[2], 2) if stats[2] else 0
    
    # Distribution par rayon
    cursor.execute("SELECT rayon, COUNT(*) FROM mesures WHERE rayon IS NOT NULL GROUP BY rayon")
    rayons = cursor.fetchall()
    
    # Dernières entrées (5 plus récentes)
    cursor.execute("SELECT id, poids, date, rayon FROM mesures ORDER BY date DESC LIMIT 5")
    dernieres_entrees = cursor.fetchall()
    
    conn.close()

    # Préparer les données pour la page HTML
    data = []
    for p in produits:
        id_produit = p[0]
        poids = p[1]
        date_str = p[2]
        rayon = p[3]
        qr_file = f"{id_produit}.png"
        data.append({
            "id": id_produit,
            "poids": poids,
            "date": date_str,
            "rayon": rayon if rayon else "N/A",
            "qr": qr_file
        })
    
    # Préparer les dernières entrées
    recent_data = []
    for p in dernieres_entrees:
        qr_file = f"{p[0]}.png"
        recent_data.append({
            "id": p[0],
            "poids": p[1],
            "date": p[2],
            "rayon": p[3] if p[3] else "N/A",
            "qr": qr_file
        })
    
    # Préparer distribution des rayons
    rayon_data = [{"rayon": r[0] if r[0] else "N/A", "count": r[1]} for r in rayons]

    return render_template("index.html", 
                         produits=data, 
                         nb_produits=nb_produits,
                         entrees_aujourdhui=entrees_aujourdhui,
                         poids_moyen=poids_moyen,
                         poids_min=poids_min,
                         poids_max=poids_max,
                         rayons=rayon_data,
                         dernieres_entrees=recent_data)

if __name__ == "__main__":
    app.run(debug=True)
