
from qualite import (
    analyser_ligne,
    analyser_lot,
    histogramme,
)


def test_piece_juste_sous_limite_basse():
    code, mesure, resultat = analyser_ligne(
        "AXE-0001 ; 24.949",
        nominal=25.0,
        tolerance=0.05
    )

    assert resultat == "rebut"


def test_code_entoure_espaces():
    code, mesure, resultat = analyser_ligne(
        "  AXE-0001  ; 25.00 "
    )

    assert code == "AXE-0001"
    assert resultat == "conforme"


def test_lot_entierement_invalide():
    lignes = [
        "mauvaise ligne",
        "AXE-0001 ; abc",
        "AXE-010 ; 25.00",
    ]

    resultats, erreurs = analyser_lot(lignes)

    assert resultats == []
    assert len(erreurs) == 3



def test_histogramme_sans_mesure():
    resultat = histogramme(
        [],
        debut=24.92,
        pas=0.02,
        nb_classes=2
    )

    assert resultat == (
        "[24.920 ; 24.940[ \n"
        "[24.940 ; 24.960[ "
    )
