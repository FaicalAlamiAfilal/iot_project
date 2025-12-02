import sqlite3

conn = sqlite3.connect("poids.db")
cursor = conn.cursor()

# Ajouter une colonne rayon si elle n'existe pas
cursor.execute("""
ALTER TABLE mesures ADD COLUMN rayon INTEGER
""")

conn.commit()
conn.close()

print("Colonne 'rayon' ajoutée à la base.")
