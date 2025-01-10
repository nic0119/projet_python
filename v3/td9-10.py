import tkinter as tk
from tkinter import ttk, messagebox
from SearchEngine import SearchEngine
from Corpus import Corpus
from datetime import datetime

#Initialisation du corpus et du moteur de recherche
corpus = Corpus("Corpus")
corpus.load('corpus.csv')
search_engine = SearchEngine(corpus)

#Fonction pour effectuer la recherche
def recherche():
    #Suppression les anciennes valeurs du tableau
    for item in tableau.get_children():
        tableau.delete(item)
    
    #Récupération des données entrées par l'utilisateur
    requete = entree_requete.get()
    n_resultats = slider_resultats.get()
    auteur = entree_auteur.get()
    date_debut = entree_date_debut.get()
    date_fin = entree_date_fin.get()

    #Validation des champs de date
    try:
        if date_debut:
            date_debut = datetime.strptime(date_debut, "%Y/%m/%d")
        if date_fin:
            date_fin = datetime.strptime(date_fin, "%Y/%m/%d")
    except ValueError:
        tk.messagebox.showerror("Erreur", "Les dates doivent être au format YYYY/MM/DD.")
        return

    #Effectue la recherche
    resultats = search_engine.search(
        requete=requete,
        n=n_resultats,
        auteur=auteur if auteur else None,
        date_debut=date_debut.strftime("%Y/%m/%d") if date_debut else None,
        date_fin=date_fin.strftime("%Y/%m/%d") if date_fin else None,
    )

    #Affichage les résultats dans le tableau
    if resultats.empty:
        tk.messagebox.showinfo("Info", "Aucun résultat trouvé.")
    else:
        for _, row in resultats.iterrows():
            tableau.insert("", "end", values=list(row))

#Création de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Moteur de recherche")
fenetre.geometry("800x600")

#Configuration de la grille pour un redimensionnement dynamique
fenetre.columnconfigure(0, weight=1)
fenetre.rowconfigure(0, weight=0)  #Cadre des champs
fenetre.rowconfigure(1, weight=0)  #Bouton
fenetre.rowconfigure(2, weight=1)  #Tableau des résultats

#Widgets pour les entrées
frame_champs = tk.Frame(fenetre)
frame_champs.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
frame_champs.columnconfigure(1, weight=1)

#Champ de texte de la requête
tk.Label(frame_champs, text="Requête :", anchor="w").grid(row=0, column=0, sticky="w", padx=5, pady=5)
entree_requete = tk.Entry(frame_champs)
entree_requete.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

#Slider du nombre de résultats
tk.Label(frame_champs, text="Nombre de résultats :", anchor="w").grid(row=1, column=0, sticky="w", padx=5, pady=5)
slider_resultats = tk.Scale(frame_champs, from_=1, to=50, orient="horizontal", length=200)  # Ajustez length pour contrôler la taille
slider_resultats.set(5)
slider_resultats.grid(row=1, column=1, sticky="w", padx=5, pady=5) 

#Champ de texte de l'auteur
tk.Label(frame_champs, text="Auteur :", anchor="w").grid(row=2, column=0, sticky="w", padx=5, pady=5)
entree_auteur = tk.Entry(frame_champs)
entree_auteur.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

#Champ de texte de la date de début
tk.Label(frame_champs, text="Date de début (YYYY/MM/DD) :", anchor="w").grid(row=3, column=0, sticky="w", padx=5, pady=5)
entree_date_debut = tk.Entry(frame_champs)
entree_date_debut.grid(row=3, column=1, sticky="ew", padx=5, pady=5)

#Champ de texte de la date de la fin
tk.Label(frame_champs, text="Date de fin (YYYY/MM/DD) :", anchor="w").grid(row=4, column=0, sticky="w", padx=5, pady=5)
entree_date_fin = tk.Entry(frame_champs)
entree_date_fin.grid(row=4, column=1, sticky="ew", padx=5, pady=5)

#Bouton pour lancer la recherche
frame_bouton = tk.Frame(fenetre)
frame_bouton.grid(row=1, column=0, pady=10, sticky="ew")
bouton_rechercher = tk.Button(frame_bouton, text="Rechercher", command=recherche)
bouton_rechercher.pack()

#Tableau d'affichage des résultats
frame_tableau = tk.Frame(fenetre)
frame_tableau.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
frame_tableau.rowconfigure(0, weight=1)
frame_tableau.columnconfigure(0, weight=1)

colonnes = ("Titre", "Auteur", "Date", "Score de Similarité")
tableau = ttk.Treeview(frame_tableau, columns=colonnes, show="headings")
for col in colonnes:
    tableau.heading(col, text=col)
    tableau.column(col, anchor="center")
tableau.grid(row=0, column=0, sticky="nsew")

#Ajout d'une barre de défilement au tableau
scrollbar_verticale = ttk.Scrollbar(frame_tableau, orient="vertical", command=tableau.yview)
scrollbar_verticale.grid(row=0, column=1, sticky="ns")
tableau.configure(yscrollcommand=scrollbar_verticale.set)

#Lancement de la boucle principale
fenetre.mainloop()
