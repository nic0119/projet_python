# Projet Python : Moteur de Recherche

**Auteurs : Nicolas Tran et Hubert Geoffray**  
**Professeur : Julien Velcin**  
**Date : 10/01/2025**  
**M1 Informatique, Université Lumière Lyon 2**

---

## Description

Ce projet consiste à développer un moteur de recherche en Python permettant :  
- L'extraction de documents depuis **Reddit** et **Arxiv** via leurs APIs.  
- La création d'un corpus filtré par mots-clés et sauvegardé en `.csv`.  
- La recherche de documents pertinents grâce à des mesures de similarité.

---

## Installation et Utilisation

1. **Créer un environnement virtuel**  
   - Sous Windows :  
     ```bash
     python -m venv env
     env\Scripts\activate
     ```  
   - Sous macOS/Linux :  
     ```bash
     python3 -m venv env
     source env/bin/activate
     ```

2. **Installation des dépendances**  
   Une fois l'environnement activé, installez les dépendances avec :  
   ```bash
   pip install -r requirements.txt

