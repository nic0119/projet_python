import praw
import urllib, urllib.request
import xmltodict
import pandas as pd
import csv
from Corpus import Corpus
from Author import Author
from Document import Document,RedditDocument, ArxivDocument
import datetime
import numpy as np
from scipy.sparse import csr_matrix
from SearchEngine import SearchEngine


id = 1
docs = []
docs2 = []
df = pd.DataFrame(columns=['id', 'texte', 'origine'])

#Alimentation des docs avec Reddit
reddit = praw.Reddit(client_id='Xf8w8k8yht4K66eNCXx9ZA', client_secret='HOuwtNXWi_hPXY2imaSjEvZ7UuaFyA', user_agent='td3')
posts = reddit.subreddit('basketball').hot(limit=25)
for post in posts:
    i = post.selftext.replace("\n", " ")
    #Si le post reddit n'a pas de "selftext", on ne l'ajoute pas
    if i != "":
        docs.append(i)
        docs2.append(("Reddit", post))
        df.loc[id] = [id, i, 'Reddit']
        id += 1

#Alimentation des docs avec Arxiv
for i in range(25):
    url = 'http://export.arxiv.org/api/query?search_query=all:electron&start={}&max_results=1'.format(i)
    data = urllib.request.urlopen(url).read()
    x = xmltodict.parse(data)
    entry = x['feed']['entry']
    summary = x['feed']['entry']['summary']
    title = x['feed']['entry']['title']
    authors = x['feed']['entry']['author']
    date = x['feed']['entry']['updated']
    url = x['feed']['link']
    if isinstance(authors, list):
        author = authors[0]['name']
        co_authors = [author['name'] for author in authors[1:]]
    else:
        auteur_principal = authors['name']
        co_authors = []
    docs.append(summary)
    docs2.append(("Arxiv", entry))
    df.loc[id] = [id, summary , 'Arxiv']
    id += 1

#Enregistrement des données dans un fichier .csv
df.to_csv('data.csv', index=False, sep='\t')


#Chargement des données enregistrées auparavant
with open('E:/m1/pyt/projet/v3/data.csv', 'r') as a:
    csvreader = csv.reader(a)
df = pd.read_csv('E:/m1/pyt/projet/v3/data.csv', sep='\t')

#Taille du corpus
print(len(df))

#Affichage du nombre de phrases et de mots pour chaque document
for doc in df["texte"]:
    print("Nombre de phrases : " + str(len(doc.split("."))))
    print("Nombre de mots : " + str(len(doc.split(" "))))

#Suppression des documents contenant moins de 20 caractères
df = df[df["texte"].str.len() >= 20]
# Affichage du nombre de documents restants
print("Nombre total de documents après suppression :", len(df))

#Chaine unique de tous les documents
chaine_unique = " ".join(df["texte"])


#Initialisation de collection pour initier id2doc
collection = []
for nature, doc in docs2:
    if nature == "Arxiv":

        titre = doc["title"].replace('\n', '')  
        co_auteurs = []
        try:
            co_auteurs = ", ".join([a["name"] for a in doc["author"][:1]])
            auteur = doc['author'][0]['name']
        except:
            auteur = doc['author']['name']  
        summary = doc["summary"].replace("\n", "")  
        date = datetime.datetime.strptime(doc["published"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y/%m/%d")  

        doc_classe = ArxivDocument(titre, auteur, date, doc["id"], summary, co_auteurs) 
        collection.append(doc_classe) 

    elif nature == "Reddit":
        titre = doc.title.replace("\n", '')
        auteur = str(doc.author)
        date = datetime.datetime.fromtimestamp(doc.created).strftime("%Y/%m/%d")
        url = "https://www.reddit.com/"+doc.permalink
        texte = doc.selftext.replace("\n", "")
        nbCom = doc.num_comments

        doc_classe = RedditDocument(titre, auteur, date, url, texte, nbCom)

        collection.append(doc_classe)


id2doc = {}
for i, doc in enumerate(collection):
    id2doc[i] = doc.titre

#Test de sauvegarde et de chargement du corpus créé
corpus = Corpus("Mon corpus")
for doc in collection:
    corpus.add(doc)
corpus.save('E:/m1/pyt/projet/v3/corpus.csv')

del corpus
corpus = Corpus("Mon corpus")
corpus.load('E:/m1/pyt/projet/v3/corpus.csv')
print(corpus)
# corpus.show(3,"123")

#Test des fonctions concorde et stats
res = corpus.concorde("ball")
print(res)

corpus.stats(10)

#Test de SearchEngine
moteur = SearchEngine(corpus)
requete = input("Entrez des mots-clés pour la recherche : ")
n = 5
resultats = moteur.search(requete, n)
print(resultats)