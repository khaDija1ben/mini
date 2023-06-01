import tkinter as tk
import tkinter.ttk as ttk
import json
from tkinter import messagebox

class Compte:
    def __init__(self, mot_de_passe, nom, prenom, solde):
        self.mot_de_passe = mot_de_passe
        self.nom = nom
        self.prenom = prenom
        self.solde = solde

    def crediter(self, montant):
        self.solde += montant

    def debiter(self, montant):
        if self.solde >= montant:
            self.solde -= montant
        else:
            print("Solde insuffisant.")

    def afficher_solde(self):
        print(f"Solde du compte : {self.solde}")

    def afficher_informations(self):
        print(f"Nom : {self.nom}")
        print(f"Prénom : {self.prenom}")
        print(f"Solde : {self.solde}")

def sauvegarder_comptes(comptes):
    with open("comptes.txt", "w") as fichier:
        for compte in comptes:
            compte_dict = {
                "mot_de_passe": compte.mot_de_passe,
                "nom": compte.nom,
                "prenom": compte.prenom,
                "solde": compte.solde
            }
            fichier.write(json.dumps(compte_dict) + "\n")

def charger_comptes():
    comptes = []

    try:
        with open("comptes.txt", "r") as fichier:
            for ligne in fichier:
                compte_dict = json.loads(ligne)
                compte = Compte(compte_dict["mot_de_passe"], compte_dict["nom"], compte_dict["prenom"], compte_dict["solde"])
                comptes.append(compte)

    except FileNotFoundError:
        # Gérer l'erreur si le fichier n'est pas trouvé
        print("Le fichier comptes.txt n'a pas été trouvé.")

    return comptes

def afficher_solde():
    compte = liste_comptes[index_compte]

    fenetre_solde = tk.Toplevel(fenetre)
    fenetre_solde.title("Solde")
    fenetre_solde.geometry("300x100")
    fenetre_solde.style = ttk.Style()
    fenetre_solde.style.theme_use("clam")

    fenetre_solde.configure(bg="#FFFFFF")  # Couleur de fond blanche

    solde_label = ttk.Label(fenetre_solde, text=f"Solde du compte : {compte.solde}", font=("Helvetica", 14, "bold"))
    solde_label.pack()

def retirer_solde():
    montant = float(montant_entry.get())
    compte = liste_comptes[index_compte]
    compte.debiter(montant)
    sauvegarder_comptes(liste_comptes)
    fenetre_retirer.destroy()
    messagebox.showinfo("Validation", "Votre opération de retrait a été effectuée avec succès.")

def transferer_argent():
    montant = float(montant_entry.get())
    compte_source = liste_comptes[index_compte]
    compte_destination = liste_comptes[destinataire_combo.current()]

    if compte_source.solde >= montant:
        compte_source.debiter(montant)
        compte_destination.crediter(montant)
        sauvegarder_comptes(liste_comptes)
        fenetre_transferer.destroy()
        messagebox.showinfo("Validation", "Votre opération de transfert a été effectuée avec succès.")
    else:
        messagebox.showerror("Erreur", "Solde insuffisant.")

def terminer():
    fenetre.destroy()

def connexion():
    mot_de_passe = mot_de_passe_entry.get()

    for i, compte in enumerate(liste_comptes):
        if compte.mot_de_passe == mot_de_passe:
            global index_compte
            index_compte = i

            fenetre_compte = tk.Toplevel(fenetre)
            fenetre_compte.title("Compte")
            fenetre_compte.geometry("300x200")
            fenetre_compte.style = ttk.Style()
            fenetre_compte.style.theme_use("clam")

            fenetre_compte.configure(bg="#EDEDED")  # Couleur de fond gris clair

            solde_button = ttk.Button(fenetre_compte, text="Solde", command=afficher_solde)
            retirer_button = ttk.Button(fenetre_compte, text="Retirer", command=ouvrir_fenetre_retrait)
            transferer_button = ttk.Button(fenetre_compte, text="Transférer", command=ouvrir_fenetre_transferer)
            terminer_button = ttk.Button(fenetre_compte, text="Terminer", command=terminer)

            solde_button.pack(pady=10)
            retirer_button.pack(pady=10)
            transferer_button.pack(pady=10)
            terminer_button.pack(pady=10)

            # Masquer la fenêtre principale
            fenetre.withdraw()

            return

    print("Mot de passe incorrect.")

def ouvrir_fenetre_retrait():
    global fenetre_retirer, montant_entry

    fenetre_retirer = tk.Toplevel(fenetre)
    fenetre_retirer.title("Retrait")
    fenetre_retirer.geometry("300x150")
    fenetre_retirer.style = ttk.Style()
    fenetre_retirer.style.theme_use("clam")

    fenetre_retirer.configure(bg="#EDEDED")  # Couleur de fond gris clair

    montant_label = ttk.Label(fenetre_retirer, text="Montant à retirer :", font=("Helvetica", 12))
    montant_entry = ttk.Entry(fenetre_retirer, font=("Helvetica", 12))
    retirer_button = ttk.Button(fenetre_retirer, text="Retirer", command=retirer_solde)

    montant_label.pack(pady=10)
    montant_entry.pack(pady=5)
    retirer_button.pack(pady=10)

def ouvrir_fenetre_transferer():
    global fenetre_transferer, montant_entry, destinataire_combo

    fenetre_transferer = tk.Toplevel(fenetre)
    fenetre_transferer.title("Transfert")
    fenetre_transferer.geometry("300x200")
    fenetre_transferer.style = ttk.Style()
    fenetre_transferer.style.theme_use("clam")

    fenetre_transferer.configure(bg="#EDEDED")  # Couleur de fond gris clair

    montant_label = ttk.Label(fenetre_transferer, text="Montant à transférer :", font=("Helvetica", 12))
    montant_entry = ttk.Entry(fenetre_transferer, font=("Helvetica", 12))

    destinataire_label = ttk.Label(fenetre_transferer, text="Destinataire :", font=("Helvetica", 12))
    destinataire_combo = ttk.Combobox(fenetre_transferer, values=[f"{compte.nom} {compte.prenom}" for compte in liste_comptes], font=("Helvetica", 12))

    transferer_button = ttk.Button(fenetre_transferer, text="Transférer", command=transferer_argent)

    montant_label.pack(pady=10)
    montant_entry.pack(pady=5)
    destinataire_label.pack(pady=10)
    destinataire_combo.pack(pady=5)
    transferer_button.pack(pady=10)

liste_comptes = charger_comptes()

fenetre = tk.Tk()
fenetre.title("Connexion")
fenetre.geometry("300x150")
fenetre.style = ttk.Style()
fenetre.style.theme_use("clam")

fenetre.configure(bg="#EDEDED")  # Couleur de fond gris clair

mot_de_passe_label = ttk.Label(fenetre, text="Mot de passe :", font=("Helvetica", 12))
mot_de_passe_entry = ttk.Entry(fenetre, show="*", font=("Helvetica", 12))
connexion_button = ttk.Button(fenetre, text="Connexion", command=connexion)

mot_de_passe_label.pack(pady=10)
mot_de_passe_entry.pack(pady=5) 
connexion_button.pack(pady=10)

fenetre.mainloop()
