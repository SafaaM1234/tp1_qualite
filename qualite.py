"""Contrôle qualité d'une ligne d'usinage : lecture des mesures, verdicts, statistiques, rapport."""
import math

NOMINAL = 25.0     # diamètre nominal des axes, en mm
TOLERANCE = 0.05   # tolérance admise : 25,00 ± 0,05 mm


# --- Étape 1 : lire les données -----------------------------------------------------------------

def lire_mesure(texte: str) -> float:
    """Convertit une mesure en nombre positif et fini."""
    texte_original = texte.strip()

    try:
        texte = texte.strip().lower()
        texte = texte.removesuffix("mm")
        texte = texte.strip()
        texte = texte.replace(",", ".")

        mesure = float(texte)

        if not math.isfinite(mesure) or mesure <= 0:
            raise ValueError

        return mesure

    except ValueError:
        raise ValueError(
            f"mesure invalide : {texte_original!r}"
        )




def valider_code(code: str) -> bool:
    
    if len(code) != 8:
        return False

    lettres = code[:3]
    tiret = code[3]
    chiffres = code[4:]

    return (
        lettres.isascii()
        and lettres.isalpha()
        and lettres.isupper()
        and tiret == "-"
        and chiffres.isascii()
        and chiffres.isdigit()
    )

    ## raise NotImplementedError("à compléter")


# --- Étape 2 : décider ----------------------------------------------------------------------------
def ecart(mesure: float, nominal: float = NOMINAL) -> float:
    """Écart à la cote nominale, arrondi au micromètre (3 décimales) pour éliminer le bruit des flottants."""
    return round(mesure - nominal, 3)


def verdict(mesure: float, nominal: float = NOMINAL, tolerance: float = TOLERANCE) -> str:
    """Renvoie "conforme", "à reprendre" (trop gros : on peut réusiner) ou "rebut" (trop petit)."""
    if tolerance <= 0:
        raise ValueError("la tolérance doit être positive")

    e = ecart(mesure, nominal)

    if abs(e) <= tolerance:
        return "conforme"
    elif e > 0:
        return "à reprendre"
    else:
        return "rebut"

    ## raise NotImplementedError("à compléter")


# --- Étape 3 : analyser une ligne -----------------------------------------------------------------
def analyser_ligne(ligne: str, *, nominal: float = NOMINAL, tolerance: float = TOLERANCE) -> tuple[str, float, str]:
    """Analyse une ligne "AXE-0042 ; 25,03 mm" et renvoie (code, mesure, verdict).

    Lève ValueError si la ligne n'a pas deux champs, si le code ou la mesure est invalide.
    """
    champs = ligne.split(";")

    if len(champs) != 2:
        raise ValueError(f"2 champs attendus, {len(champs)} trouvé(s)")

    code = champs[0].strip().upper()

    if not valider_code(code):
        raise ValueError(f"code invalide : {code!r}")

    mesure = lire_mesure(champs[1])

    resultat = verdict(
        mesure,
        nominal=nominal,
        tolerance=tolerance
    )

    return code, mesure, resultat

    ## raise NotImplementedError("à compléter")


# --- Étape 4 : analyser un lot --------------------------------------------------------------------
def analyser_lot(lignes: list[str], **reglages) -> tuple[list[tuple[str, float, str]], list[str]]:
    """Analyse toutes les lignes d'un lot et renvoie (resultats, erreurs).

    Les lignes vides et les commentaires (#) sont ignorés. Une ligne invalide n'arrête pas l'analyse :
    son message est ajouté à erreurs, sous la forme "ligne 4 : mesure invalide : 'abc'".
    Les réglages (nominal, tolerance) sont transmis tels quels à analyser_ligne.
    """
    resultats = []
    erreurs = []

    for numero, ligne in enumerate(lignes, start=1):

        # Ignorer les lignes vides et les commentaires
        if not ligne.strip() or ligne.lstrip().startswith("#"):
            continue

        try:
            resultat = analyser_ligne(ligne, **reglages)
            resultats.append(resultat)

        except ValueError as err:
            erreurs.append(f"ligne {numero} : {err}")

    return resultats, erreurs



def compter_verdicts(resultats: list[tuple[str, float, str]]) -> tuple[int, int, int]:
    """Renvoie le nombre de pièces (conformes, à reprendre, rebuts)."""
    
    conformes = 0
    reprises = 0
    rebuts = 0

    for code, mesure, resultat in resultats:
        if resultat == "conforme":
            conformes += 1
        elif resultat == "à reprendre":
            reprises += 1
        elif resultat == "rebut":
            rebuts += 1

    return conformes, reprises, rebuts



# --- Étape 5 : statistiques et capabilité ---------------------------------------------------------
def moyenne(*valeurs: float) -> float:
    """Moyenne d'un nombre quelconque de valeurs. Lève ValueError s'il n'y en a aucune."""
    raise NotImplementedError("à compléter")


def ecart_type(*valeurs: float) -> float:
    """Écart type d'échantillon (division par n - 1). Lève ValueError avec moins de deux valeurs."""
    raise NotImplementedError("à compléter")


def capabilite(mesures: list[float], *, nominal: float = NOMINAL, tolerance: float = TOLERANCE) -> tuple[float, float]:
    """Indices de capabilité (Cp, Cpk), arrondis à 2 décimales.

    Cp  = largeur de la tolérance / (6 sigma)                  : le procédé est-il assez précis ?
    Cpk = distance de la moyenne à la limite la plus proche / (3 sigma) : est-il bien centré ?
    """
    raise NotImplementedError("à compléter")


# --- Étape 6 : le rapport -------------------------------------------------------------------------
def rapport(lignes: list[str], *, nominal: float = NOMINAL, tolerance: float = TOLERANCE) -> str:
    """Construit le rapport de contrôle d'un lot, sous forme d'une seule chaîne (une ligne par pièce)."""
    raise NotImplementedError("à compléter")


# --- Étape 8 (à la maison) : histogramme ----------------------------------------------------------
def histogramme(mesures: list[float], *, debut: float, pas: float, nb_classes: int) -> str:
    """Histogramme texte : une ligne par classe [borne, borne + pas[, une étoile par mesure.

    Les mesures hors de [debut, debut + nb_classes * pas[ sont ignorées.
    """
    raise NotImplementedError("à compléter")
