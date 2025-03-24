employes = {}

def ajoute_employe():
    identifiant = input("Entrer le numéro d'identifiant: ")
    if identifiant in employes:
        print ("Cet identifiant est déja pris veuillez en selectionner un autre")
        return
    nom = input("Entrer le nom de la personne: ")
    employes[identifiant] = nom
    print(f"L'employé {nom} a été ajouté avec succès")

def affiche_employe():
    if not employes:
        print("Le nom de la personne n'existe pas")
    else :
        print("\nListe des employés :")
        for identifiant, nom in employes.items():
            print(f"{identifiant} : {nom}")

def supprimer_employe(valeur):
    """Supprime un employé par ID ou par nom."""
    if valeur.isdigit():  # Suppression par ID
        id = int(valeur)
        if id in employes:
            print(f"🗑️ Suppression de {employes[id]} (ID: {id}).")
            del employes[id]
        else:
            print("❌ Aucun employé trouvé avec cet ID.")
    else:  # Suppression par nom
        found = False
        for id, nom in list(employes.items()):
            if nom.lower() == valeur.lower():
                print(f"🗑️ Suppression de {nom} (ID: {id}).")
                del employes[id]
                found = True
                break
        if not found:
            print("❌ Aucun employé trouvé avec ce nom.")


def menu():
    """Affiche le menu et gère les interactions utilisateur."""
    while True:
        print("\n--- Menu Gestion des Employés ---")
        print("1️⃣ Ajouter un employé")
        print("2️⃣ Afficher la liste des employés")
        print("3️⃣ Supprimer un employé")
        print("4️⃣ Quitter")

        choix = input("👉 Votre choix : ").strip()

        match choix:
            case "1":
                ajoute_employe()

            case "2":
                affiche_employe()

            case "3":
                valeur = input("🗑️ Entrez le nom ou l'ID de l'employé à supprimer : ").strip()
                supprimer_employe(valeur)

            case "4":
                print("👋 Au revoir !")
                sys.exit()

            case _:
                print("❌ Choix invalide. Veuillez entrer un chiffre entre 1 et 4.")

# Lancer le programme
menu()