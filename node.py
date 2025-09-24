# node.py
class Node:
    def __init__(self, country, iso3, values):
        self.country = country
        self.iso3 = iso3
        self.values = values  # lista F1961..F2022

        # Redondeamos la media a 2 decimales para que búsquedas exactas funcionen.
        self.mean = round(sum(values) / len(values), 2)

        # Propiedades AVL
        self.height = 1
        self.left = None
        self.right = None
        self.parent = None
