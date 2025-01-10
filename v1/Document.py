class Document:
    #Initialisation du document
    def __init__(self, titre, auteur, date, url, texte, type=""):
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte
        self.type = type
    
    #Retourne le titre
    def __str__(self):
        return self.titre
    
    #Retourne le type du document
    def getType(self):
        return self.type



class RedditDocument(Document):
    #Initialisation du post Reddit
    def __init__(self, titre="", auteur="", date="", url="", texte="", nbCom = 0):
        super().__init__(titre, auteur, date, url, texte)
        self.nbCom = nbCom

    #Renvoie les infos principales du document
    def __str__(self):
        return (f"Post Reddit: {self.titre}, par {self.auteur}, le {self.date}, "
                f"{self.nbCom} commentaires. URL: {self.url}")

    #Renvoie le nombre de commentaires
    def getNbCom(self):
        return self.nbCom
    
    #Permet de changer la variable de nombre de commentaires
    def setNbCom(self, nbCom = 0):
        self.nbCom = nbCom

    #Renvoie le type "Reddit" à la classe mère
    def getType(self):
        return "Reddit"



class ArxivDocument(Document):
    #Initialisation du document Arxiv
    def __init__(self, titre="", auteur="", date="", url="", texte="", co_auteurs = None):
        super().__init__(titre, auteur, date, url , texte)
        self.co_auteurs = co_auteurs if co_auteurs else []

    #Renvoie les infos principales du document
    def __str__(self):
        co_auteurs = ", ".join(self.co_auteurs) if self.co_auteurs else "Aucun co-auteur"
        return (f"Article ArXiv: {self.titre}, par {self.auteur} et co-auteurs: {co_auteurs}, "
                f"publié le {self.date}. URL: {self.url}")

    #Renvoie le nom des co-auteurs
    def getCoAuteurs(self):
        return self.co_auteurs
    
    #Permet de changer la variable des co-auteurs
    def setCoAuteurs(self, co_auteurs):
        self.co_auteurs = co_auteurs
        
    #Renvoie le type "Arxiv" à la classe mère
    def getType(self):
        return "Arxiv"