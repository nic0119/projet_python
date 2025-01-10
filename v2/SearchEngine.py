import numpy as np
from scipy.sparse import csr_matrix
import pandas as pd

class SearchEngine:
    def __init__(self, corpus):
        #Initialisation et construction du vocabulaire
        self.corpus = corpus
        self.vocab = {}
        self.mots_uniques = set()

        for doc in corpus.id2doc.values():
            texte_nettoye = corpus.nettoyer_texte(doc['text'])
            mots = texte_nettoye.split()
            self.mots_uniques.update(mots)

        self.mots_tries = sorted(self.mots_uniques)
        for idx, mot in enumerate(self.mots_tries):
            self.vocab[mot] = {'id': idx, 'occurrences_totales': 0, 'documents_contenant': 0}

        #Construction de la matrice TF
        self.n_docs = len(corpus.id2doc) #Nombre total de documents
        self.n_mots = len(self.vocab) #Nombre total de mots
        doc_ids, mot_ids, freq = [], [], [] #Initialisation des données pour la matrice TF

        for doc_id, doc in enumerate(corpus.id2doc.values()):
            texte_nettoye = corpus.nettoyer_texte(doc['text'])
            mots = texte_nettoye.split()
            compteur = {}
            #Comptage des occurrences des mots dans chaque document
            for mot in mots:
                if mot in self.vocab:
                    compteur[mot] = compteur.get(mot, 0) + 1
            #Remplissage des matrices
            for mot, count in compteur.items():
                doc_ids.append(doc_id)
                mot_ids.append(self.vocab[mot]['id'])
                freq.append(count)
        #Matrice TF
        #Si erreur de chargement de la matrice TF, enlever le commentaire de la ligne suivante
        #doc_ids = [doc_id - 1 for doc_id in doc_ids]
        self.mat_TF = csr_matrix((freq, (doc_ids, mot_ids)), shape=(self.n_docs, self.n_mots))

        #Calcul des occurences totales et du nombre de documents contenant un mot spécifique
        occurrences_totales = np.array(self.mat_TF.sum(axis=0)).flatten()
        documents_contenant = np.array((self.mat_TF > 0).sum(axis=0)).flatten()
  
        for mot, data in self.vocab.items():
            data['occurrences_totales'] = occurrences_totales[data['id']]
            data['documents_contenant'] = documents_contenant[data['id']]

        #Matrice TF-IDF
        idf = np.log(self.n_docs / (1 + documents_contenant))
        self.mat_TFxIDF = self.mat_TF.multiply(idf).tocsr()

    def search(self, requete, n=5):
        #Nettoyage et vecteur pour la requête
        requete = self.corpus.nettoyer_texte(requete)
        vecteur_requete = [0] * len(self.vocab)

        #Vérification de la présence des mots dans la requête
        for mot in requete:
            if mot in self.vocab:
                vecteur_requete[self.vocab[mot]['id']] = 1

        similarites = []

        for doc_id, doc in self.corpus.id2doc.items():
            #Initialisation des vecteurs document
            texte_nettoye = self.corpus.nettoyer_texte(doc['text'])
            vecteur_document = [0] * len(self.vocab)
            for mot in texte_nettoye:
                if mot in self.vocab:
                    vecteur_document[self.vocab[mot]['id']] = 1

            #Calcul du produit scalaire et des normes
            produit = np.dot(vecteur_requete, vecteur_document)
            norme_requete = np.linalg.norm(vecteur_requete)
            norme_document = np.linalg.norm(vecteur_document)

            #Calcul des similarités
            if norme_requete == 0 or norme_document == 0:
                similarite = 0
            else:
                similarite = produit / (norme_requete * norme_document)

            similarites.append((doc_id, similarite))

        #Tri par ordre décroissant
        similarites.sort(key=lambda x: x[1], reverse=True)

        #Récupération des résultats les plus pertinents
        resultats = []
        for doc_id, score in similarites[:n]:
            doc = self.corpus.id2doc[doc_id]
            resultats.append([doc['title'], score])

        #Conversion en DataFrame
        df_resultats = pd.DataFrame(resultats, columns=["Titre", "Score de Similarité"])
        return df_resultats
