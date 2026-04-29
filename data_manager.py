import json
import os

class DataManager:
    def __init__(self, fichier='contenus.json'):
        self.fichier = fichier
        if not os.path.exists(fichier):
            with open(fichier, 'w') as f:
                json.dump([], f)

    def lire_tous(self):
        with open(self.fichier, 'r') as f:
            return json.load(f)

    def sauvegarder(self, data):
        with open(self.fichier, 'w') as f:
            json.dump(data, f, indent=4)

    def ajouter(self, contenu):
        data = self.lire_tous()
        data.append(contenu)
        self.sauvegarder(data)

    def trouver_par_id(self, id):
        for c in self.lire_tous():
            if c['id'] == id:
                return c

    def mettre_a_jour(self, id, new):
        data = self.lire_tous()
        for i, c in enumerate(data):
            if c['id'] == id:
                data[i] = new
        self.sauvegarder(data)

    def supprimer(self, id):
        data = [c for c in self.lire_tous() if c['id'] != id]
        self.sauvegarder(data)