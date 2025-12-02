import random
from datetime import datetime
import sqlite3
import qrcode
import os
def generer_poids():
    return round(random.uniform(700, 750), 2)  # valeurs entre 700g et 750g



# ---------------------------
# 1. Connexion à la base
# ---------------------------
conn = sqlite3.connect("poids.db")
cursor = conn.cursor()

# ---------------------------

# Créer le dossier si il n'existe pas
os.makedirs("static/qr_codes", exist_ok=True)

# 2. Fonction pour simuler un poids
# ---------------------------
def simuler_poids():
    return round(random.uniform(700, 750), 2)  # g

# ---------------------------
# 3. Fonction pour générer un rayon aléatoire
# ---------------------------
def generer_rayon():
    return random.randint(1, 6)  # 1 à 6

# ---------------------------
# 4. Simulation
# ---------------------------
resultats = []  # liste vide pour stocker les produits

for i in range(20):
    poids = simuler_poids()
    rayon = generer_rayon()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    resultats.append({
    "Produit": i+1,
    "Poids": poids,
    "Rayon": rayon
})


    # Enregistrement dans SQLite
    cursor.execute(
        "INSERT INTO mesures (poids, date, rayon) VALUES (?, ?, ?)",
        (poids, timestamp, rayon)
    )
    conn.commit()

    # Contenu du QR
    texte_qr = (
        f"Produit : {i+1}\n"
        f"Poids : {poids} g\n"
        f"Rayon : {rayon}\n"
        f"Date : {timestamp}"
    )
    print("Nombre de produits captés :", len(resultats))


    # Génération du QR code
    img = qrcode.make(texte_qr)
    img.save(f"static/qr_codes/qr_produit_{i+1}.png")


    print(f"Produit {i+1} → {poids} g → Rayon {rayon} → QR généré")

# Fermeture
conn.close()


