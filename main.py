"""Programme principal : un petit terminal de contrôle qualité, piloté par des commandes."""
from donnees import LOT_A
from qualite import analyser_ligne, rapport

AIDE = """Commandes :
  mesure CODE VALEUR   contrôler une pièce (ex. : mesure AXE-0100 25,04)
  lot                  rapport du lot A
  aide                 afficher cette aide
  quitter              terminer"""


def executer(commande: str, saisies: list[str]) -> bool:
    """Exécute une commande ; renvoie False quand il faut quitter."""
   
    commande = commande.strip()

    # Si l'utilisateur ne tape rien
    if not commande:
        return True

    # Séparer la commande en mots
    morceaux = commande.split()
    action = morceaux[0].lower()

    # 1. Commande quitter
    if action == "quitter":
        print(f"{len(saisies)} pièce(s) contrôlée(s) à la main. Au revoir.")
        return False

    # 2. Commande aide
    elif action == "aide":
        print(AIDE)
        return True

    # 3. Commande lot
    elif action == "lot":
        if len(morceaux) != 1:
            print("Erreur : la commande lot ne prend aucun argument.")
        else:
            print(rapport(LOT_A + saisies))
        return True

    # 4. Commande mesure
    elif action == "mesure":
        if len(morceaux) != 3:
            print("Commande inconnue ou incomplète. Tapez aide.")
            return True

        code = morceaux[1]
        valeur = morceaux[2]

        try:
            # Analyser la pièce avec les fonctions déjà créées
            code, mesure, resultat = analyser_ligne(
                f"{code};{valeur}"
            )

            # Conserver la mesure pour le rapport du lot
            saisies.append(f"{code};{valeur}")

            # Afficher le résultat du contrôle
            print(f"{code} : {mesure:.3f} mm -> {resultat}")

        except ValueError as erreur:
            print(f"Refusé : {erreur}")

        return True

    # 5. Commande inconnue
    else:
        print("Commande inconnue. Tapez aide pour voir les commandes.")
        return True



def main() -> None:
    print("Contrôle qualité, ligne 2. Tapez aide pour la liste des commandes.")
    saisies: list[str] = []
    continuer = True
    while continuer:
        continuer = executer(input("> ").strip(), saisies)


if __name__ == "__main__":
    main()
