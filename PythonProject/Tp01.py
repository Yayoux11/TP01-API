#!/usr/bin/env python3

import requests
import sys

# URL de l'API choisie
API_URL = "https://data.economie.gouv.fr/api/explore/v2.0/catalog/datasets/rappelconso0/records?limit=10&offset=0&timezone=UTC"


def fetch_data(url):
    """
    Récupère les données depuis l’API.

    Args:
        url (str): L’URL de l’API.

    Returns:
        dict: La réponse JSON convertie en dictionnaire.

    En cas d’erreur (connexion, timeout, code HTTP != 200), affiche un message et quitte.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Déclenche une exception pour les codes d'erreur HTTP
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Erreur lors de la requête à l'API :", e)
        sys.exit(1)


def filter_records(records, filter_field=None, filter_value=None):
    """
    Filtre les enregistrements selon un champ et une valeur donnés.

    Args:
        records (list): Liste d'enregistrements (dictionnaires) extraits de la réponse API.
        filter_field (str): Le nom du champ sur lequel appliquer le filtre.
        filter_value (str): La valeur à rechercher dans le champ.

    Returns:
        list: Liste des enregistrements filtrés.
    """
    if not filter_field or not filter_value:
        return records

    filtered = []
    for record in records:
        # Récupération du dictionnaire "fields" de chaque enregistrement
        fields = record.get('record', {}).get('fields', {})
        field_value = fields.get(filter_field, "")
        # Comparaison insensible à la casse
        if filter_value.lower() in str(field_value).lower():
            filtered.append(record)
    return filtered


def display_records(records):
    """
    Affiche les enregistrements de manière lisible dans la console.

    Args:
        records (list): Liste d'enregistrements à afficher.
    """
    if not records:
        print("Aucun résultat trouvé.")
        return

    for record in records:
        fields = record.get('record', {}).get('fields', {})
        print("--------------------------------------------------")
        print("Libellé               :", fields.get("libelle", "N/A"))
        print("Référence Fiche       :", fields.get("reference_fiche", "N/A"))
        print("Catégorie de produit  :", fields.get("categorie_de_produit", "N/A"))
        print("Marque                :", fields.get("nom_de_la_marque_du_produit", "N/A"))
        print("Motif du rappel       :", fields.get("motif_du_rappel", "N/A"))
        print("Lien fiche rappel     :", fields.get("lien_vers_la_fiche_rappel", "N/A"))
        print("--------------------------------------------------\n")


def get_user_filter():
    """
    Récupère les critères de filtrage saisis par l'utilisateur.

    Returns:
        tuple: (filter_field, filter_value) ou (None, None) si aucun filtrage.
    """
    print("Voulez-vous filtrer les résultats ? (oui/non)")
    choice = input().strip().lower()
    if choice not in ["oui", "o", "yes", "y"]:
        return None, None

    print("Sur quel champ souhaitez-vous filtrer ?")
    print("Options disponibles : categorie_de_produit, nom_de_la_marque_du_produit, libelle")
    filter_field = input("Champ : ").strip()
    if filter_field not in ["categorie_de_produit", "nom_de_la_marque_du_produit", "libelle"]:
        print("Champ non valide. Aucun filtrage ne sera appliqué.")
        return None, None

    filter_value = input("Entrez la valeur à rechercher : ").strip()
    if not filter_value:
        print("Valeur vide. Aucun filtrage ne sera appliqué.")
        return None, None

    return filter_field, filter_value


def run_tests():
    """
    Effectue quelques tests de validation sur les fonctions principales.
    """
    print("Exécution des tests...")
    # Test de récupération de données
    data = fetch_data(API_URL)
    assert isinstance(data, dict), "La réponse de l'API doit être un dictionnaire."
    assert "records" in data, "La réponse doit contenir la clé 'records'."

    # Test du filtrage (exemple sur 'categorie_de_produit')
    records = data.get("records", [])
    filtered = filter_records(records, "categorie_de_produit", "Alimentation")
    assert isinstance(filtered, list), "Le résultat du filtrage doit être une liste."

    print("Tous les tests sont passés avec succès.\n")


def main():
    """
    Fonction principale exécutant le client API.
    """
    print("Récupération des données depuis l'API...")
    data = fetch_data(API_URL)
    records = data.get("records", [])

    # Demande à l'utilisateur s'il souhaite filtrer les résultats
    filter_field, filter_value = get_user_filter()
    if filter_field and filter_value:
        records = filter_records(records, filter_field, filter_value)

    # Affichage des résultats
    display_records(records)


if __name__ == '__main__':
    # Décommentez la ligne suivante pour exécuter les tests avant d'utiliser le programme.
    # run_tests()

    main()
