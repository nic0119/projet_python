from Author import Author
import pandas as pd
import re
from Document import ArxivDocument,RedditDocument

class Corpus:
    #Initialisation du corpus
    def __init__(self, nom):
        self.nom = nom
        self.authors = {}
        self.aut2id = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0
        self.resultats = None
        self.co_authors = {}
        self.nb_comments = {}

    #Ajout d'un document au corpus
    def add(self, doc):
        if doc.auteur not in self.aut2id:
            self.naut += 1
            self.authors[self.naut] = Author(doc.auteur)
            self.aut2id[doc.auteur] = self.naut
        self.authors[self.aut2id[doc.auteur]].add(doc.texte)

        self.id2doc[self.ndoc] = {
            'doc_id': self.ndoc + 1,
            'title': doc.titre,
            'author': doc.auteur,
            'text': doc.texte,
            'date': doc.date,
            'type': doc.getType(),
            'co_authors': doc.getCoAuteurs() if isinstance(doc, ArxivDocument) else [],
            'nb_comments': doc.getNbCom() if isinstance(doc, RedditDocument) else 0
        }
        self.ndoc += 1

    #Affichage des n premiers documents selon un ordre spécifique
    def show(self, n_docs=-1, tri="abc"):
        docs = list(self.id2doc.values())
        if tri == "abc": 
            docs = sorted(docs, key=lambda x: x['title'].lower())[:n_docs]
        elif tri == "123": 
            docs = sorted(docs, key=lambda x: x['date'])[:n_docs]

        print("\n".join([f"{doc['title']} ({doc['date']}) - {doc['author']}" for doc in docs]))

    #Renvoie le titre, la date et l'auteur de chaque document
    def __repr__(self):
        docs = list(self.id2doc.values())
        docs = sorted(docs, key=lambda x: x['title'].lower())

        return "\n".join([f"{doc['title']} ({doc['date']}) - {doc['author']}" for doc in docs])

    #Sauvegarde du corpus dans un fichier .csv
    def save(self, filepath):
        #Initialisation des données à sauvegarder
        data = {
            'doc_id': [],
            'title': [],
            'author': [],
            'text': [],
            'date': [],
            'type': [],
            'co_authors': [],
            'nb_comments': []
        }

        #Remplissage des données avec les informations des documents
        for doc_id, doc in self.id2doc.items():
            data['doc_id'].append(doc_id)
            data['title'].append(doc['title'])
            data['author'].append(doc['author'])
            data['text'].append(doc['text'])
            data['date'].append(doc['date']),
            if doc['type'] == 'Arxiv':
                data['type'].append('Arxiv')
                data['co_authors'].append(", ".join(self.co_authors.get(doc['title'], [])))
                data['nb_comments'].append("")
            elif doc['type'] == 'Reddit':
                data['type'].append('Reddit')
                data['co_authors'].append("")
                data['nb_comments'].append(self.nb_comments.get(doc['title'], 0))

        df = pd.DataFrame(data)
        df.to_csv(filepath, index=False)

    #Chargement du corpus à partir d'un fichier .csv
    def load(self, filepath):
        df = pd.read_csv(filepath)

        #Réinitialisation du corpus
        self.nom = filepath
        self.ndoc = 0
        self.authors = {}
        self.aut2id = {}
        self.id2doc = {}
        self.naut = 0

        #Remplissage du corpus
        for idx, row in df.iterrows():
            auteur = row['author']
            texte = row['text']

            if auteur not in self.aut2id:
                self.naut += 1
                self.authors[self.naut] = Author(auteur)
                self.aut2id[auteur] = self.naut

            self.authors[self.aut2id[auteur]].add(texte)

            #Ajout d'un document au corpus
            self.ndoc += 1
            self.id2doc[self.ndoc] = {
                'doc_id': row['doc_id'],
                'title': row['title'],
                'author': auteur,
                'text': texte,
                'date': row['date']
            }


    #Recherche d'un mot-clé dans le corpus
    def search(self, mot_cle):
        #Construction de la variable rsultats si inexistante
        if self.resultats is None:
            self.resultats = " ".join([str(doc['text']) for doc in self.id2doc.values()])

        #Expression régulière pour rechercher le mot-clé
        exp_reg = rf"\b{re.escape(mot_cle)}\b" 
        res = re.findall(rf".*?{exp_reg}.*?(?:\.|\n|$)", self.resultats)

        return res
    
    #Recherche dans le corpus avec contecte autour
    def concorde(self, expression, taille_contexte=30):
        #Construction de la variable rsultats si inexistante
        if self.resultats is None:
            self.resultats = " ".join([str(doc['text']) for doc in self.id2doc.values()])
            
        #Expression régulière pour rechercher l'expression avec un contexte autour
        exp_reg = rf"(.{{0,{taille_contexte}}})({re.escape(expression)})(.{{0,{taille_contexte}}})"
        res = re.findall(exp_reg, self.resultats)
        df = pd.DataFrame(res, columns=["contexte gauche", "motif trouvé", "contexte droit"])
        return df
    
    #Nettoyage du texte
    def nettoyer_texte(self, txt):
        #Si txt n'est pas une chaine de caractère, on convertie txt en chaine de caractères
        if not isinstance(txt, str):
            txt = str(txt)
        txt = txt.lower() #Texte mis en miniscule
        txt = txt.replace('\n', ' ') #Suppressiont des passages à la ligne
        txt = re.sub(r'[^\w\s]', ' ', txt) #Suppression de la ponctuation
        txt = re.sub(r'\s+', ' ', txt).strip() #Remplacement des espaces multiples par un espace simple et suppression des espaces en début et fin de chaine
        return txt    

    #Calcul du nombre de mots différents dans le corpus et des plus fréquents
    def stats(self, n=10):
        mots = []

        #Parcourt les documents pour collecter les mots
        for doc in self.id2doc.values():
            texte_nettoye = self.nettoyer_texte(doc['text'])
            mots.extend(texte_nettoye.split())  # Ajouter tous les mots du document

        #Calcul de la fréquence des mots (TF) avec pandas
        freq = pd.Series(mots).value_counts()

        #Création d'un DataFrame pour les fréquences
        df_freq = pd.DataFrame({
            'Mot': freq.index,
            'Fréquence': freq.values
        })

        #Tri des mots par fréquence décroissante
        df_freq = df_freq.sort_values(by='Fréquence', ascending=False)

        #Affichage des statistiques
        print(f"Nombre de mots différents dans le corpus : {len(freq)}")
        print(f"Les {n} mots les plus fréquents :\n")
        print(df_freq.head(n))

        return df_freq