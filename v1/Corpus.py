from Author import Author
import pandas as pd
import re

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
            'date': doc.date
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
            'date': []
        }
        #Remplissage des données avec les informations des documents
        for doc_id, doc in self.id2doc.items():
            data['doc_id'].append(doc_id)
            data['title'].append(doc['title'])
            data['author'].append(doc['author'])
            data['text'].append(doc['text'])
            data['date'].append(doc['date'])

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

