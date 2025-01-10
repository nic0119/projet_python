class Author:
    #Initialisation de l'auteur
    def __init__(self, name):
        self.name = name
        self.ndoc = 0
        self.production = []

    #Ajout d'un document écrit par l'auteur
    def add(self, production):
        self.ndoc += 1
        self.production.append(production)
        
    #Retourne le nom de l'auteur et son nombre de documents écrits 
    def __str__(self):
        return f"Auteur : {self.name}\t# productions : {self.ndoc}"
    
    #Renvoie le nombre de documents écrits par l"auteur et leur taille moyenne
    def stats(self):
        if self.ndoc == 0:
            return "Aucun document produit."
        total_length = sum([len(doc.texte) for doc in self.production.values()])
        avg_length = total_length / self.ndoc if self.ndoc > 0 else 0
        return f"Nombre de documents : {self.ndoc}, Taille moyenne des documents : {avg_length} caractères"