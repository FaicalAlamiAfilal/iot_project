import sqlite3

conn = sqlite3.connect("poids.db")
cursor = conn.cursor()

# Vérifier si la table existe
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables dans la base :", tables)

# Vérifier le contenu de la table mesures
cursor.execute("SELECT * FROM mesures")
rows = cursor.fetchall()
print("Contenu de la table mesures :", rows)

conn.close()
